from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import ListaEspera, EstadoListaEspera 
from django.shortcuts import render, get_object_or_404, redirect
from turnos.models import ClaseProgramada
from reservas.models import Reserva 
from reservas.models import EstadoReserva

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
                ListaEspera.objects.create(
                    user=request.user,
                    clase_programada=clase_programada,
                )
                messages.success(request, 'Te anotaste en la lista de espera.')
            else:
                messages.warning(request, 'Ya tenés una inscripción activa en la lista de espera.')
        else:
            ListaEspera.objects.create(
                user=request.user,
                clase_programada=clase_programada,
            )
            messages.success(request, 'Te anotaste en la lista de espera.')

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

@login_required
def confirmar_desde_email(request, lista_espera_id):
    """Muestra la notificación enviada por email y permite confirmar o cancelar."""

    entrada = get_object_or_404(ListaEspera, pk=lista_espera_id, user=request.user)

    if entrada.estado != EstadoListaEspera.NOTIFICADO:
        messages.error(request, 'Este enlace ya no es válido.')
        return redirect('reservas_disponibles')

    if request.method == 'POST':
        accion = request.POST.get('accion')

        if accion == 'confirmar':
            if Reserva.objects.filter(
                user=entrada.user,
                clase_programada=entrada.clase_programada,
                estado=EstadoReserva.ACTIVA
            ).exists():
                messages.warning(request, 'Ya tenés una reserva activa para esta clase.')
            else:
                Reserva.objects.create(
                    user=entrada.user,
                    clase_programada=entrada.clase_programada,
                    estado=EstadoReserva.ACTIVA
                )
                entrada.estado = EstadoListaEspera.CONFIRMADO
                entrada.save()
                messages.success(request, '¡Confirmado! Tu lugar está reservado.')

            return redirect('reservas_disponibles')

        if accion == 'cancelar':
            entrada.estado = EstadoListaEspera.CANCELADO
            entrada.save()

            from lista_espera.tasks import notificar_siguiente
            notificar_siguiente.delay(entrada.clase_programada.id)

            messages.success(request, 'Cancelaste la notificación y liberaste el cupo para la siguiente persona.')
            return redirect('reservas_disponibles')

        messages.error(request, 'Acción inválida.')
        return redirect('reservas_disponibles')

    return render(request, 'notificacion_email.html', {
        'entrada': entrada,
        'clase_programada': entrada.clase_programada,
    })

