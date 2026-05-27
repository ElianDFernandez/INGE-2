from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from django.contrib import messages
from django.urls import reverse

from .models import Reserva, EstadoReserva
from .forms import ReservaCancelForm, ReservaForm

from actividades.models import Actividad
from turnos.models import Clase, ClaseProgramada


def clases_disponibles(request):
    for clase in Clase.objects.all():
        for i in range(14): 
            fecha = timezone.localdate() + timedelta(days=i)
            if fecha.weekday() == clase.dia_numero():
                # si no existía la creo
                ClaseProgramada.objects.get_or_create(clase=clase, fecha=fecha) 
    
    actividades = Actividad.objects.prefetch_related('turno_set__clase_set')
    # --- NUEVA LÓGICA PARA EL BOTÓN ---
    clases_reservadas_ids = []
    if request.user.is_authenticated:
        # Buscamos las reservas activas de este usuario y sacamos solo los IDs de las clases
        clases_reservadas_ids = Reserva.objects.filter(
            user=request.user
        ).exclude(
            estado=EstadoReserva.CANCELADA
        ).values_list('clase_programada_id', flat=True)

    return render(request, 'clases_disponibles.html', {
        'actividades': actividades,
        'clases_reservadas_ids': list(clases_reservadas_ids) # Lo pasamos al HTML
    })

@login_required
def reserva_confirm(request, clase_programada_pk):
    clase_programada = get_object_or_404(ClaseProgramada, pk=clase_programada_pk)

    if request.method == 'POST':
        form = ReservaForm(request.POST, user=request.user, clase_programada=clase_programada)

        if form.is_valid():
            reserva = form.save(commit=False)

            reserva.user = request.user
            reserva.clase_programada = clase_programada

            reserva.save()
            return redirect('clases_disponibles')

    else:
        form = ReservaForm(user=request.user, clase_programada=clase_programada)

    return render(request, 'reservas/reserva_confirm.html', {'form': form, 'clase_programada': clase_programada})

@login_required
def reserva_list(request):
    reservas = Reserva.objects.filter(user=request.user).select_related('clase_programada__clase__turno__actividad')
    return render(request, 'reservas/reserva_list.html', {'reservas': reservas})

@login_required
def reserva_cancel(request, reserva_pk):
    reserva = get_object_or_404(Reserva, pk=reserva_pk, user=request.user)

    if request.method == 'POST':
        form = ReservaCancelForm(request.POST)
        if form.is_valid():
            reserva.estado = EstadoReserva.CANCELADA
            reserva.fecha_cancelacion = timezone.now()
            reserva.save()
            return redirect('reserva_list')
    else:
        form = ReservaCancelForm()

    return render(request, 'reservas/reserva_cancel.html', {'form': form, 'reserva': reserva})




