from datetime import datetime, timedelta
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Prefetch
from django.contrib import messages
from django.urls import reverse
from lista_espera.models import ListaEspera, EstadoListaEspera
import mercadopago
from django.conf import settings
from django.http import HttpResponse

from io import BytesIO
import qrcode

from .models import Reserva, EstadoReserva, Inscripcion
from .forms import ReservaCancelForm, ReservaForm, InscripcionCancelForm, InscripcionForm

from actividades.models import Actividad
from turnos.models import Turno, Clase, ClaseProgramada

URL_NGROK =  "https://handstand-aghast-left.ngrok-free.dev"

@login_required
def reservas_disponibles(request):
    hoy = timezone.localdate()
    # CLASES INDIVIDUALES
    clases_programadas = ClaseProgramada.objects.filter(fecha__gte=hoy, clase__activo=True, clase__turno__activo=True).select_related('clase', 'clase__turno', 'clase__turno__actividad').order_by('fecha', 'clase__hora_inicio')
    clases_reservadas_ids = Reserva.objects.filter(user=request.user, estado=EstadoReserva.ACTIVA).values_list('clase_programada_id', flat=True)
    #Clases de lista de espera (filtrado por estados)
    clases_en_lista_espera_cancelados = ListaEspera.objects.filter(user=request.user,estado=EstadoListaEspera.CANCELADO).values_list('clase_programada_id', flat=True)
    clases_en_lista_espera_ids = ListaEspera.objects.filter(user=request.user,estado=EstadoListaEspera.PENDIENTE).values_list('clase_programada_id', flat=True)
    
    clases_reservadas_ids = Reserva.objects.filter(user=request.user, estado__in=[EstadoReserva.ACTIVA, EstadoReserva.PENDIENTE_PAGO]).values_list('clase_programada_id', flat=True)
    clases_programadas = [cp for cp in clases_programadas if cp.puede_reservarse]

    # TURNOS
    turnos = Turno.objects.filter(activo=True).select_related('actividad').prefetch_related(
        Prefetch('clase_set', queryset=Clase.objects.filter(activo=True).order_by('dia', 'hora_inicio').prefetch_related(
            Prefetch('claseprogramada_set', queryset=ClaseProgramada.objects.filter(fecha__gte=hoy).order_by('fecha'))
        ))
    )
    turnos_filtrados = []
    for turno in turnos:
        turno.usuario_inscripto = turno.esta_inscripto(request.user)
        tiene_clase_reservable = False
        for clase in turno.clase_set.all():
            for cp in clase.claseprogramada_set.all():
                if cp.puede_reservarse:
                    tiene_clase_reservable = True
                    break
            if tiene_clase_reservable:
                break
        if tiene_clase_reservable:
            turnos_filtrados.append(turno)
    turnos = turnos_filtrados

    actividades_filtro = Actividad.objects.all().order_by('nombre')

    inscripciones_ids = Inscripcion.objects.filter(
        user=request.user,
        estado='ACTIVA'
    ).values_list('turno_id', flat=True)

    #me devuelve el cupo ocupado y disponible de la clase para la lista de espera (activa, seña pagada y notificados)
    for clase in clases_programadas:
        reservas_ocupadas = Reserva.objects.filter(
            clase_programada=clase,
            estado__in=[EstadoReserva.ACTIVA, EstadoReserva.PENDIENTE_PAGO]
        ).count()

        notificados = ListaEspera.objects.filter(
            clase_programada=clase,
            estado=EstadoListaEspera.NOTIFICADO
        ).count()

        ocupadas = reservas_ocupadas + notificados
        clase.cupo_ocupado = ocupadas
        clase.cupo_real = clase.clase.cupo_maximo - ocupadas
        
        #calcula posicion en lista de espera
        entrada_lista = ListaEspera.objects.filter(
        clase_programada=clase,
        user=request.user,
        estado=EstadoListaEspera.PENDIENTE).first()
    
        if entrada_lista:
            clase.posicion_lista = ListaEspera.objects.filter(
                clase_programada=clase,
                estado=EstadoListaEspera.PENDIENTE,
                fecha_anotacion__lt=entrada_lista.fecha_anotacion).count() + 1
        else:
            clase.posicion_lista = None
        

    return render(request, 'reservas_disponibles.html', {
        'clases_programadas': clases_programadas,
        'clases_reservadas_ids': list(clases_reservadas_ids),
        'clases_en_lista_espera_ids': list(clases_en_lista_espera_ids),
        'clases_canceladas_lista_espera_ids': list(clases_en_lista_espera_cancelados),
        'turnos': turnos,
        'inscripciones_ids': list(inscripciones_ids),
        'actividades_filtro': actividades_filtro
    })

@login_required
def reserva_confirm(request, clase_programada_pk):
    clase_programada = get_object_or_404(ClaseProgramada, pk=clase_programada_pk, clase__activo=True, clase__turno__activo=True)
    
    # Validar que no tenga ya una reserva activa/señada para esta clase
    ya_reservado = Reserva.objects.filter(
        user=request.user,
        clase_programada=clase_programada,
        estado__in=[EstadoReserva.ACTIVA, EstadoReserva.PENDIENTE_PAGO]
    ).exists()
    if ya_reservado:
        messages.warning(request, 'Ya tenés una reserva para esta clase.')
        return redirect('reservas_disponibles')

    # Validar que haya cupo disponible
    if clase_programada.cupo_actual() >= clase_programada.clase.cupo_maximo:
        messages.error(request, 'No hay cupo disponible para esta clase.')
        return redirect('reservas_disponibles')

    # Verificar vales disponibles para esta actividad
    actividad = clase_programada.clase.turno.actividad
    vales_disponibles = request.user.vales.filter(
        actividad=actividad,
        usado=False,
        fecha_vencimiento__gte=timezone.localdate()
    )
    tiene_vales = vales_disponibles.exists()

    if request.method == 'POST':
        form = ReservaForm(request.POST, user=request.user, clase_programada=clase_programada)
        if form.is_valid():
            usar_vale = 'usar_vale' in request.POST

            if usar_vale and tiene_vales:
                # CASO: Usar vale → crear reserva ACTIVA directamente, sin pasar por MP
                vale = vales_disponibles.first()
                vale.usar()

                reserva = Reserva.objects.create(
                    user=request.user,
                    clase_programada=clase_programada,
                    estado=EstadoReserva.ACTIVA,
                    pago_confirmado=True,
                )

                messages.success(request, f'Reserva confirmada con vale. Vale para {actividad.nombre} utilizado.')
                return redirect('reserva_list')

            else:
                # CASO: Pago normal por MercadoPago (seña 50%)
                reserva = form.save(commit=False)
                reserva.user = request.user
                reserva.clase_programada = clase_programada
                reserva.estado = 'INICIADA' 
                reserva.pago_confirmado = False
                reserva.save()
                
                valor_total = float(clase_programada.clase.costo)
                valor_sena = valor_total * 0.50
                
                sdk = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)

                url_exito = f"{URL_NGROK}/reservas/reserva/{reserva.id}/pago-exitoso/"
                url_fallo = f"{URL_NGROK}/reservas/reserva/{reserva.id}/pago-fallido/"

                preference_data = {
                    "items": [
                        {
                            "title": f"Seña Reserva: {clase_programada.clase.turno.actividad.nombre}",
                            "quantity": 1,
                            "unit_price": float(valor_sena),
                        }
                    ],
                    "back_urls": {
                        "success": url_exito,
                        "failure": url_fallo,
                        "pending": url_fallo
                    },
                    "auto_return": "approved",
                }
           
                try:
                    preference_response = sdk.preference().create(preference_data)
                    print(">>> RESPUESTA CRUDA DE MP:", preference_response)
                    preference = preference_response["response"]
                    
                    reserva.mp_preference_id = preference['id']
                    reserva.save()
                    
                    return redirect(preference['sandbox_init_point']) 

                except Exception as e:
                    print(">>> ERROR EN PYTHON:", e)
                    reserva.delete()
                    messages.error(request, 'Error en el pago de la seña. No se ha podido establecer la conexión. Intente más tarde.')
                    return redirect('reservas_disponibles')
    else:
        form = ReservaForm(user=request.user, clase_programada=clase_programada)

    valor_sena = float(clase_programada.clase.costo) * 0.50

    return render(request, 'reservas/reserva_confirm.html', {
        'form': form,
        'clase_programada': clase_programada,
        'valor_sena': valor_sena,
        'tiene_vales': tiene_vales,
        'vales_disponibles': vales_disponibles,
    })

@login_required
def pago_exitoso(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    payment_id = request.GET.get('payment_id')
    
    if payment_id:
        reserva.mp_payment_id = payment_id
        
        # ESCENARIO 1: Acaba de pagar la seña (el primer 50%)
        if reserva.estado == 'INICIADA':
            reserva.estado = 'PENDIENTE_PAGO'
            
        # ESCENARIO 2: Acaba de pagar el restante (el segundo 50%)
        elif reserva.estado == 'PENDIENTE_PAGO':
            reserva.estado = 'ACTIVA'
            reserva.pago_confirmado = True # Pagó el 100%
            
        reserva.save()
        #Nota : restar cupo donde?
    
    messages.success(request, 'La operación se realizó correctamente. Tu reserva está confirmada.')
    return redirect('reserva_list')

@login_required
def pago_fallido(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id, user=request.user)
    
    if reserva.estado == 'INICIADA':
        # Nunca pagó nada → cancelamos la reserva y volvemos a la vista de reservas disponibles
        reserva.estado = EstadoReserva.CANCELADA
        reserva.save()
        messages.error(request, 'El pago no pudo procesarse.')
        return redirect('reservas_disponibles')
    elif reserva.estado == 'PENDIENTE_PAGO':
        # Ya pagó la seña, falló el restante → se mantiene con seña pagada
        messages.warning(request, 'El pago del restante no pudo procesarse. Tu reserva sigue activa con la seña abonada.')
        return redirect('reserva_list')

@login_required
def reserva_list(request):
    hoy = timezone.localdate()
    reservas = Reserva.objects.filter(user=request.user).select_related('clase_programada__clase__turno__actividad').order_by('clase_programada__fecha', 'clase_programada__clase__hora_inicio').exclude(estado='INICIADA')
    inscripciones = Inscripcion.objects.filter(user=request.user)
    return render(request, 'reservas/reserva_list.html', {
        'reservas': reservas, 
        'inscripciones': inscripciones
    })

@login_required
def reserva_cancel(request, reserva_pk):
    reserva = get_object_or_404(Reserva, pk=reserva_pk, user=request.user, estado__in=[EstadoReserva.ACTIVA, EstadoReserva.PENDIENTE_PAGO])

    # Determina si es abonado (inscripto al turno de esta clase)
    turno = reserva.clase_programada.clase.turno
    es_abonado = Inscripcion.objects.filter(
        user=request.user, turno=turno, estado='ACTIVA'
    ).exists()

    # Calcular anticipación para saber qué pasará
    ahora = timezone.now()
    fecha_hora_clase = datetime.combine(
        reserva.clase_programada.fecha,
        reserva.clase_programada.clase.hora_inicio
    )
    fecha_hora_clase = timezone.make_aware(fecha_hora_clase, timezone.get_current_timezone())
    anticipacion = fecha_hora_clase - ahora

    pagado = reserva.estado in (EstadoReserva.ACTIVA, EstadoReserva.PENDIENTE_PAGO)
    pago_total = reserva.estado == EstadoReserva.ACTIVA
    pagado_con_vale = pago_total and not reserva.mp_payment_id

    if es_abonado:
        if pago_total and anticipacion >= timedelta(hours=48):
            resultado_cancelacion = 'vale'
        elif pagado:
            resultado_cancelacion = 'pierde'
        else:
            resultado_cancelacion = 'sin_pago'
    else:
        if pagado and anticipacion >= timedelta(hours=24) and not pagado_con_vale:
            resultado_cancelacion = 'devuelve_total' if pago_total else 'devuelve_sena'
        elif pagado and not pagado_con_vale:
            resultado_cancelacion = 'pierde_total' if pago_total else 'pierde_sena'
        else:
            resultado_cancelacion = 'sin_pago'

    if request.method == 'POST':
        form = ReservaCancelForm(request.POST)
        if form.is_valid():
            reserva.estado = EstadoReserva.CANCELADA
            reserva.fecha_cancelacion = ahora
            reserva.save()

            #Cuando se cancela una clase envia mensaje a los usuarios en lista de espera para esa clase
            if ListaEspera.objects.filter(
                clase_programada=reserva.clase_programada,
                estado=EstadoListaEspera.PENDIENTE
            ).exists():
                from lista_espera.tasks import notificar_siguiente
                notificar_siguiente.delay(reserva.clase_programada.id)


            if resultado_cancelacion == 'vale':
                from socios.models import Vale
                import calendar as cal
                hoy = timezone.localdate()
                _, ultimo_dia = cal.monthrange(hoy.year, hoy.month)
                Vale.objects.create(
                    socio_id=request.user.id,
                    actividad=turno.actividad,
                    fecha_vencimiento=hoy.replace(day=ultimo_dia)
                )
                reserva.sena_devuelta = True
                messages.success(request, 'Clase cancelada. Se generó un vale para la actividad.')
            elif resultado_cancelacion == 'pierde':
                messages.warning(request, 'Clase cancelada. No se genera vale por cancelar con menos de 48hs de anticipación.')
            elif resultado_cancelacion == 'devuelve_total':
                reserva.devolver_pago()
                return redirect('simular_reembolso', reserva_pk=reserva.pk)
            elif resultado_cancelacion == 'devuelve_sena':
                reserva.devolver_pago()
                return redirect('simular_reembolso', reserva_pk=reserva.pk)
            elif resultado_cancelacion == 'pierde_total':
                messages.warning(request, 'Reserva cancelada. El pago se pierde por cancelar con menos de 24hs de anticipación.')
            elif resultado_cancelacion == 'pierde_sena':
                messages.warning(request, 'Reserva cancelada. La seña se pierde por cancelar con menos de 24hs de anticipación.')
            else:
                messages.success(request, 'Reserva cancelada correctamente.')

            reserva.save()

            return redirect('reserva_list')
    else:
        form = ReservaCancelForm()

    return render(request, 'reservas/reserva_cancel.html', {
        'form': form,
        'reserva': reserva,
        'es_abonado': es_abonado,
        'resultado_cancelacion': resultado_cancelacion,
    })

@login_required
def inscripcion_confirm(request, turno_pk):
    turno = get_object_or_404(Turno, pk=turno_pk, activo=True)
    clases = turno.get_clases_programadas().filter(fecha__gte=timezone.localdate()).exclude(
        reserva__user=request.user,
        reserva__estado=EstadoReserva.ACTIVA
    )

    inscripcion_temp = Inscripcion(user=request.user, turno=turno)
    costo_total = float(inscripcion_temp.get_costo())
    valor_a_pagar = float(inscripcion_temp.get_costo_final())
    descuento = costo_total - valor_a_pagar

    # Costo bruto: todas las clases futuras sin importar estado
    todas_futuras = turno.get_clases_programadas().filter(fecha__gte=timezone.localdate())
    costo_total_bruto = sum(float(cp.clase.costo) for cp in todas_futuras)

    # Calcular total ya pagado sobre TODAS las clases futuras (incluye ACTIVA)
    total_ya_pagado = 0.0
    for cp in todas_futuras:
        reserva = Reserva.objects.filter(
            user=request.user,
            clase_programada=cp
        ).exclude(estado=EstadoReserva.CANCELADA).first()

        if reserva and reserva.estado == EstadoReserva.ACTIVA:
            total_ya_pagado += float(cp.clase.costo)
        elif reserva and reserva.estado == EstadoReserva.PENDIENTE_PAGO:
            total_ya_pagado += float(cp.clase.costo) * 0.50

    # Construir lista con estado de pago para mostrar en template
    clases_con_estado = []
    for cp in clases:
        clases_con_estado.append({
            'clase_programada': cp,
        })

    if request.method == 'POST':
        ya_inscripto = Inscripcion.objects.filter(
            user=request.user, turno=turno, estado__in=['ACTIVA', 'INICIADA']
        ).exists()
        if ya_inscripto:
            messages.warning(request, 'Ya tenés una inscripción activa o en proceso para este turno.')
            return redirect('reservas_disponibles')
        if valor_a_pagar <= 0:
            messages.warning(request, 'No hay clases disponibles para inscribirse.')
            return redirect('reservas_disponibles')
        inscripcion = Inscripcion.objects.create(
            user=request.user,
            turno=turno,
            estado='INICIADA'
        )

        sdk = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)

        url_exito = f"{URL_NGROK}/reservas/inscripcion/{inscripcion.id}/pago-exitoso/"
        url_fallo = f"{URL_NGROK}/reservas/inscripcion/{inscripcion.id}/pago-fallido/"

        preference_data = {
            "items": [
                {
                    "title": f"Inscripción: {turno.nombre} - {turno.actividad.nombre}",
                    "quantity": 1,
                    "unit_price": valor_a_pagar,
                }
            ],
            "back_urls": {
                "success": url_exito,
                "failure": url_fallo,
                "pending": url_fallo
            },
            "auto_return": "approved",
        }

        try:
            preference_response = sdk.preference().create(preference_data)
            preference = preference_response["response"]

            inscripcion.mp_preference_id = preference['id']
            inscripcion.save()

            return redirect(preference['sandbox_init_point'])

        except Exception as e:
            print(">>> ERROR EN PYTHON:", e)
            inscripcion.delete()
            messages.error(request, 'Error en el pago. No se ha podido establecer la conexión. Intente más tarde.')
            return redirect('reservas_disponibles')

    return render(request, 'inscripciones/inscripcion_confirm.html', {
        'turno': turno,
        'clases_con_estado': clases_con_estado,
        'costo_total_bruto': costo_total_bruto,
        'total_ya_pagado': total_ya_pagado,
        'valor_a_pagar': valor_a_pagar,
        'descuento': descuento,
    })

@login_required
def inscripcion_cancel(request, inscripcion_pk):
    inscripcion = get_object_or_404(Inscripcion, pk=inscripcion_pk, user=request.user, estado='ACTIVA')
    # muestro que clases se cancelarían si se cancela la inscripcion al turno (solo las activas)
    clases_a_cancelar = inscripcion.turno.get_clases_programadas().filter(
        fecha__gte=timezone.localdate(),
        reserva__user=request.user,
        reserva__estado=EstadoReserva.ACTIVA
    )

    if request.method == 'POST':
        form = InscripcionCancelForm(request.POST)
        if form.is_valid():
            vales_generados = inscripcion.cancelar()

            if vales_generados > 0:
                messages.success(request, f'Inscripción cancelada. Se generaron {vales_generados} vale{"s" if vales_generados > 1 else ""} para {inscripcion.turno.actividad.nombre}.')
            else:
                messages.success(request, 'Inscripción cancelada correctamente.')
            return redirect('reserva_list')
    else:
        form = InscripcionCancelForm()

    return render(request, 'inscripciones/inscripcion_cancel.html', {
        'form': form,
        'inscripcion': inscripcion,
        'clases_a_cancelar': clases_a_cancelar
    })

@login_required
def inscripcion_pago_exitoso(request, inscripcion_id):
    inscripcion = get_object_or_404(Inscripcion, id=inscripcion_id, user=request.user)
    payment_id = request.GET.get('payment_id')

    if payment_id:
        inscripcion.mp_payment_id = payment_id
        inscripcion.estado = 'ACTIVA'
        inscripcion.save()

        inscripcion.reservar_clases_programadas()

        messages.success(request, f'¡Genial! Te inscribiste con éxito al turno {inscripcion.turno.nombre} de {inscripcion.turno.actividad.nombre}.')
    else:
        messages.warning(request, 'Pago recibido pero sin ID de transacción. Contactá soporte.')

    return redirect('reserva_list')

@login_required
def inscripcion_pago_fallido(request, inscripcion_id):
    inscripcion = get_object_or_404(Inscripcion, id=inscripcion_id, user=request.user)
    inscripcion.delete()
    messages.error(request, 'El pago no pudo procesarse. Tu inscripción ha sido cancelada.')
    return redirect('reservas_disponibles')

@login_required
def simular_reembolso(request, reserva_pk):
    """Simula una pantalla de devolución de MercadoPago."""
    reserva = get_object_or_404(
        Reserva.objects.select_related('clase_programada__clase__turno__actividad'),
        pk=reserva_pk,
        user=request.user
    )

    if not reserva.corresponde_devolucion:
        messages.warning(request, 'No corresponde devolución para esta reserva.')
        return redirect('reserva_list')

    monto_devuelto = reserva.clase_programada.clase.costo
    if not reserva.pago_confirmado:
        monto_devuelto = monto_devuelto / 2

    return render(request, 'reservas/simular_reembolso.html', {
        'reserva': reserva,
        'monto_devuelto': monto_devuelto,
    })

@login_required
def pagar_restante(request, reserva_id):
    sdk = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)
    reserva = get_object_or_404(Reserva, id=reserva_id, user=request.user)
    
    # Asegurarnos de que solo se pueda pagar el restante si está en el estado correcto
    if reserva.estado != EstadoReserva.PENDIENTE_PAGO:
        # Si alguien quiere hacer trampa, lo mandamos de vuelta
        return redirect('reserva_list')

    precio_total = reserva.clase_programada.clase.costo
    valor_restante = float(precio_total) / 2.0 
    
    url_exito = f"{URL_NGROK}/reservas/reserva/{reserva.id}/pago-exitoso/"
    url_fallo = f"{URL_NGROK}/reservas/reserva/{reserva.id}/pago-fallido/"

    preference_data = {
        "items": [
            {
                "title": f"Pago Restante: {reserva.clase_programada.clase.turno.actividad.nombre}",
                "quantity": 1,
                "unit_price": valor_restante,
            }
        ],
        "back_urls": {
            "success": url_exito,
            "failure": url_fallo,
            "pending": url_fallo
        },
        "auto_return": "approved",
    }
    
    preference_response = sdk.preference().create(preference_data)
    preference = preference_response["response"]
    
    return redirect(preference['sandbox_init_point'])
def reserva_qr(request, reserva_pk):
    reserva = get_object_or_404(Reserva, pk=reserva_pk, user=request.user, estado=EstadoReserva.ACTIVA)
    
    # por si intento meterme por url
    if not reserva.clase_programada.puede_pasar_presente:
        return redirect('reserva_list')
    
    return render(request, 'reservas/reserva_qr.html', {'reserva': reserva})

@login_required
def reserva_qr_image(request, reserva_pk):
    reserva = get_object_or_404(Reserva, pk=reserva_pk, user=request.user, estado=EstadoReserva.ACTIVA)

    # por si intento meterme por url
    if not reserva.clase_programada.puede_pasar_presente:
        return redirect('reserva_list')

    imagen = qrcode.make(str(reserva.qr_token))
    buffer = BytesIO() # no quiero guardar un archivo fisico, lo guardo en memoria
    imagen.save(buffer, format="PNG")
    
    return HttpResponse(buffer.getvalue(), content_type="image/png")

@staff_member_required
def escanear_qr(request):
    return render(request, 'escanear_qr.html')


@staff_member_required
def confirmar_asistencia(request, qr_token):
    import uuid

    # escaneo cualquier otra cosa que no sea un uuid
    try:
        qr_token = uuid.UUID(qr_token)
    except ValueError:
        messages.error(request, "El código QR escaneado no es válido.")
        return redirect("escanear_qr")
    
    reserva = Reserva.objects.filter(
        qr_token=qr_token,
        estado=EstadoReserva.ACTIVA, asistio=False
    ).first()

    # si escanee un uuid, pero no esta asociada a una reserva activa en el sistema
    if reserva is None:
        messages.error(request, "El código QR escaneado no es válido.")
        return redirect("escanear_qr")

    # la reserva existe pero ya no se puede pasar asistencia
    if not reserva.clase_programada.puede_pasar_presente:
        messages.error(request, "El periodo para pasar la asistencia de esta reserva ya pasó o aún no ha comenzado.")
        return redirect("escanear_qr")

    if request.method == "POST":
        reserva.asistio = True
        reserva.metodo_asistencia = 'QR'
        reserva.save()

        messages.success(request, f"Asistencia confirmada para {reserva.user.username}.")
        return redirect("escanear_qr")

    return render(request, "confirmar_asistencia.html", {"reserva": reserva})
