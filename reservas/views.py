from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Prefetch

from django.contrib import messages
from django.urls import reverse

from .models import Reserva, EstadoReserva, Inscripcion
from .forms import ReservaCancelForm, ReservaForm, InscripcionCancelForm, InscripcionForm

from actividades.models import Actividad
from turnos.models import Turno, Clase, ClaseProgramada


@login_required
def clases_disponibles(request):
    hoy = timezone.localdate()
    actividades = Actividad.objects.prefetch_related(
        Prefetch('turno_set', queryset=Turno.objects.filter(activo=True).prefetch_related(
        Prefetch('clase_set', queryset=Clase.objects.filter(activo=True).prefetch_related(
        Prefetch('claseprogramada_set', queryset=ClaseProgramada.objects.filter(fecha__gte=hoy)))))))

    clases_reservadas_ids = []
    if request.user.is_authenticated:
        # Buscamos las reservas activas de este usuario y sacamos solo los IDs de las clases
        clases_reservadas_ids = Reserva.objects.filter(
            user=request.user
        ).filter(
            estado=EstadoReserva.ACTIVA
        ).values_list('clase_programada_id', flat=True)

    return render(request, 'clases_disponibles.html', {
        'actividades': actividades,
        'clases_reservadas_ids': list(clases_reservadas_ids) # Lo pasamos al HTML
    })

@login_required
def reserva_confirm(request, clase_programada_pk):
    clase_programada = get_object_or_404(ClaseProgramada, pk=clase_programada_pk, clase__activo=True, clase__turno__activo=True)

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
    inscripciones = Inscripcion.objects.filter(user=request.user)
    return render(request, 'reservas/reserva_list.html', {'reservas': reservas, 'inscripciones': inscripciones})

@login_required
def reserva_cancel(request, reserva_pk):
    reserva = get_object_or_404(Reserva, pk=reserva_pk, user=request.user, estado='ACTIVA')

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


@login_required
def turnos_disponibles(request):
    hoy = timezone.localdate()

    turnos = Turno.objects.filter(activo=True).select_related('actividad').prefetch_related(
        Prefetch('clase_set', queryset=Clase.objects.filter(activo=True).prefetch_related(
        Prefetch('claseprogramada_set', queryset=ClaseProgramada.objects.filter(fecha__gte=hoy)))))

    turnos_validos = []

    # nomas muestro turnos que tienen cupo en todas las clases programadas de este me
    for turno in turnos:
        if(turno.admite_inscripcion(request.user)):
            turnos_validos.append(turno)

    # me quedo con las inscripciones del usuario asi no le permito volver a inscribirse a esos turnos
    inscripciones_ids = Inscripcion.objects.filter(
        user=request.user,
        estado='ACTIVA'
    ).values_list('turno_id', flat=True) # flat para pasar de tuplas con una sola componente a enteros

    return render(request, 'turnos_disponibles.html', {
        'turnos': turnos_validos,
        'inscripciones_ids': list(inscripciones_ids)
    })

@login_required
def inscripcion_confirm(request, turno_pk):
    turno = get_object_or_404(Turno, pk=turno_pk, activo=True)
    # muestro que clases se van a reservar si se inscribe al turno (excepto las que ya estan reservadas)
    clases = turno.get_clases_programadas().filter(fecha__gte=timezone.localdate()).exclude(
        reserva__user = request.user,
        reserva__estado = EstadoReserva.ACTIVA
    )

    if request.method == 'POST':
        form = InscripcionForm(request.POST, user=request.user, turno=turno)

        if form.is_valid():
            inscripcion = form.save(commit=False)
            inscripcion.user = request.user
            inscripcion.turno = turno
            inscripcion.save()

            inscripcion.reservar_clases_programadas()
            return redirect('turnos_disponibles')
    else:
        form = InscripcionForm(user=request.user, turno=turno)

    return render(request, 'inscripciones/inscripcion_confirm.html', {
        'form': form,
        'turno': turno,
        'clases_a_reservar': clases
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
            inscripcion.estado = 'DE_BAJA'
            inscripcion.fecha_baja = timezone.now()
            inscripcion.save()

            inscripcion.cancelar_clases_programadas()
            return redirect('reserva_list')
    else:
        form = InscripcionCancelForm()

    return render(request, 'inscripciones/inscripcion_cancel.html', {
        'form': form,
        'inscripcion': inscripcion,
        'clases_a_cancelar': clases_a_cancelar
    })