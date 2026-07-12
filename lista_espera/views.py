import mercadopago
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from .models import ListaEspera, EstadoListaEspera
from turnos.models import ClaseProgramada
from reservas.models import Reserva, EstadoReserva

URL_NGROK = "https://handstand-aghast-left.ngrok-free.dev"

@login_required
def inscribirse_lista_espera(request, clase_programada_pk):
    clase_programada = get_object_or_404(ClaseProgramada, pk=clase_programada_pk)

    if request.method == 'POST':
        entrada_existente = ListaEspera.objects.filter(
            user=request.user,
            clase_programada=clase_programada
        ).first()

        if entrada_existente:
            if entrada_existente.estado == EstadoListaEspera.PENDIENTE:
                messages.warning(request, 'Ya estás en la lista de espera.')
            elif entrada_existente.estado in (EstadoListaEspera.CANCELADO, EstadoListaEspera.EXPIRADO):
                entrada_existente.delete()
                nueva_entrada=ListaEspera.objects.create(
                    user=request.user,
                    clase_programada=clase_programada,
                )
                posicion=nueva_entrada.get_posicion()
                messages.success(request, f'Te anotaste en la lista de espera.Tu posicion en espera es: #{posicion} ')
            else:
                messages.warning(request, 'Ya tenés una inscripción activa en la lista de espera.')
        else:
            nueva_entrada = ListaEspera.objects.create(
                user=request.user,
                clase_programada=clase_programada,
            )
            posicion = nueva_entrada.get_posicion()
            messages.success(request, f'Te anotaste en la lista de espera. Tu posición en espera es: #{posicion}')

        return redirect('reservas_disponibles')

    return render(request, 'lista_espera/confirmar_inscripcion_lista.html', {'clase_programada': clase_programada})


@login_required
def cancelar_lista_espera(request, clase_programada_pk):
    entrada = ListaEspera.objects.filter(
        user=request.user,
        clase_programada_id=clase_programada_pk,
        estado=EstadoListaEspera.PENDIENTE
    ).first()

    if request.method == 'POST':
        if entrada:
            entrada.delete()
            messages.success(request, 'Saliste de la lista de espera.')
        else:
            messages.warning(request, 'No se encontró tu inscripción en la lista de espera.')

    return redirect('reservas_disponibles')

#Muchos if's,lo se xd 
@login_required
def confirmar_desde_email(request, lista_espera_id):
    """Muestra la notificación enviada por email y permite confirmar o cancelar."""

    #Si cancelo y vuelvo a querer confirmar  
    entrada = ListaEspera.objects.filter(pk=lista_espera_id).first()
    if not entrada:
        messages.error(request, 'La notificación ya no es válida.')
        return redirect('reservas_disponibles')
    
    from django.utils import timezone
    if entrada.clase_programada.fecha < timezone.localdate():
        messages.error(request, 'Esta clase ya pasó, el enlace no es válido.')
        return redirect('reservas_disponibles')
    
    #Si entro con un usuario diferente al que recibió el email,muy minucioso 
    if entrada.user != request.user:
        messages.error(request, 'Iniciá sesión con la cuenta que recibió el email para confirmar esta reserva.')
        return redirect('reservas_disponibles')
    
    #Si mi tiempo de confirmacion expira
    if entrada.estado == EstadoListaEspera.NOTIFICADO and not entrada.puede_confirmar():
        entrada.estado = EstadoListaEspera.EXPIRADO
        entrada.save()

        from lista_espera.tasks import notificar_siguiente
        notificar_siguiente.delay(entrada.clase_programada.id)

        messages.error(request, 'El plazo de confirmación expiró. El cupo se ofreció al siguiente socio.')
        return redirect('reservas_disponibles')
    
    #Si el enlace no esta disponible 
    if entrada.estado != EstadoListaEspera.NOTIFICADO:
        messages.error(request, 'Este enlace ya no es válido.')
        return redirect('reservas_disponibles')
    
    actividad = entrada.clase_programada.clase.turno.actividad
    vales_disponibles = request.user.vales.filter(actividad=actividad,usado=False,fecha_vencimiento__gte=timezone.localdate())
    
    #Flujo normal,validaciones de pago y uso de vales 
    if request.method == 'POST':
        accion = request.POST.get('accion')

        if accion == 'confirmar':
            
            if Reserva.objects.filter(
                user=entrada.user,
                clase_programada=entrada.clase_programada,
                estado=EstadoReserva.INICIADA
            ).exists():
                messages.warning(request, 'Ya tenés un pago en proceso para esta clase.')
                return redirect('reservas_disponibles')

            if Reserva.objects.filter(
                user=entrada.user,
                clase_programada=entrada.clase_programada,
                estado__in=[EstadoReserva.ACTIVA, EstadoReserva.PENDIENTE_PAGO]
            ).exists():
                messages.warning(request, 'Ya tenés una reserva activa o pendiente para esta clase.')
                return redirect('reservas_disponibles')

            actividad = entrada.clase_programada.clase.turno.actividad
            tiene_vales = vales_disponibles.exists()
            usar_vale = 'usar_vale' in request.POST and tiene_vales

            if usar_vale:
                vale = vales_disponibles.first()
                vale.usar()

                reserva = Reserva.objects.create(
                    user=entrada.user,
                    clase_programada=entrada.clase_programada,
                    estado=EstadoReserva.ACTIVA,
                    pago_confirmado=True,
                )

                entrada.estado = EstadoListaEspera.CONFIRMADO
                entrada.save()

                messages.success(request, f'Reserva confirmada con vale. Vale para {actividad.nombre} utilizado.')
                return redirect('reservas_disponibles')

            reserva = Reserva.objects.create(
                user=entrada.user,
                clase_programada=entrada.clase_programada,
                estado=EstadoReserva.INICIADA,
                pago_confirmado=False,
            )

            valor_total = float(entrada.clase_programada.clase.costo)
            valor_sena = valor_total * 0.50
            sdk = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)

            url_exito = f"{URL_NGROK}{reverse('pago_exitoso_lista_espera', args=[entrada.id, reserva.id])}"
            url_fallo = f"{URL_NGROK}{reverse('pago_fallido_lista_espera', args=[entrada.id, reserva.id])}"

            preference_data = {
                'items': [
                    {
                        'title': f'Seña Reserva: {entrada.clase_programada.clase.turno.actividad.nombre}',
                        'quantity': 1,
                        'unit_price': float(valor_sena),
                    }
                ],
                'back_urls': {
                    'success': url_exito,
                    'failure': url_fallo,
                    'pending': url_fallo,
                },
                'auto_return': 'approved',
            }

            try:
                preference_response = sdk.preference().create(preference_data)
                preference = preference_response['response']
                reserva.mp_preference_id = preference['id']
                reserva.save(update_fields=['mp_preference_id'])
                return redirect(preference['sandbox_init_point'])

            except Exception:
                reserva.estado = EstadoReserva.CANCELADA
                reserva.save()
                messages.error(request, 'No se pudo iniciar el pago de la seña. Intentá nuevamente.')
                return redirect('reservas_disponibles')

        if accion == 'cancelar':
            entrada.estado = EstadoListaEspera.CANCELADO
            entrada.save()

            from lista_espera.tasks import notificar_siguiente
            notificar_siguiente.delay(entrada.clase_programada.id)

            messages.success(request, 'Cancelaste la confirmacion de esta clase.')
            return redirect('reservas_disponibles')

        messages.error(request, 'Acción inválida.')
        return redirect('reservas_disponibles')

    return render(request, 'notificacion_email.html', {
        'entrada': entrada,
        'clase_programada': entrada.clase_programada,
        'tiene_vales' : vales_disponibles.exists(),
        'vales' : vales_disponibles
    })


@login_required
def pago_exitoso_lista_espera(request, lista_espera_id, reserva_id):
    entrada = get_object_or_404(ListaEspera, pk=lista_espera_id, user=request.user)
    reserva = get_object_or_404(Reserva, pk=reserva_id, user=request.user)

    payment_id = request.GET.get('payment_id')
    if payment_id:
        reserva.mp_payment_id = payment_id

    if not entrada.puede_confirmar():
        if reserva.estado == EstadoReserva.INICIADA:
            reserva.estado = EstadoReserva.CANCELADA
            reserva.save()

        entrada.estado = EstadoListaEspera.EXPIRADO
        entrada.save()

        from lista_espera.tasks import notificar_siguiente
        notificar_siguiente.delay(entrada.clase_programada.id)

        messages.error(request, 'El plazo de confirmación expiró. El cupo se ofreció al siguiente socio.')
        return redirect('reservas_disponibles')

    if reserva.estado == EstadoReserva.INICIADA:
        reserva.estado = EstadoReserva.PENDIENTE_PAGO
        reserva.pago_confirmado = False
        reserva.save()

    entrada.estado = EstadoListaEspera.CONFIRMADO
    entrada.save()

    messages.success(request, 'Pago aceptado. Tu reserva fue realizada con exito.')
    return redirect('reservas_disponibles')


@login_required
def pago_fallido_lista_espera(request, lista_espera_id, reserva_id):
    entrada = get_object_or_404(ListaEspera, pk=lista_espera_id, user=request.user)
    reserva = get_object_or_404(Reserva, pk=reserva_id, user=request.user)

    if not entrada.puede_confirmar():
        if reserva.estado == EstadoReserva.INICIADA:
            reserva.estado = EstadoReserva.CANCELADA
            reserva.save()

        entrada.estado = EstadoListaEspera.CANCELADO
        entrada.save()

        from lista_espera.tasks import notificar_siguiente
        notificar_siguiente.delay(entrada.clase_programada.id)

        messages.error(request, 'El plazo de confirmación expiró. El cupo se ofreció al siguiente socio.')
        return redirect('reservas_disponibles')

    if reserva.estado == EstadoReserva.INICIADA:
        reserva.estado = EstadoReserva.CANCELADA
        reserva.save()

    messages.warning(request, 'El pago no pudo completarse. La reserva no pudo ser completada. Por favor intenta nuevamente.')
    return redirect('reservas_disponibles')

