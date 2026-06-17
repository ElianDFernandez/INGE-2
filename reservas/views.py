from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Prefetch
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponse

from io import BytesIO
import qrcode

from .models import Reserva, EstadoReserva, Inscripcion
from .forms import ReservaCancelForm, ReservaForm, InscripcionCancelForm, InscripcionForm

from actividades.models import Actividad
from turnos.models import Turno, Clase, ClaseProgramada

@login_required
def reservas_disponibles(request):
    hoy = timezone.localdate()
    # CLASES INDIVIDUALES
    clases_programadas = ClaseProgramada.objects.filter(fecha__gte=hoy, clase__activo=True, clase__turno__activo=True).select_related('clase', 'clase__turno', 'clase__turno__actividad').order_by('fecha', 'clase__hora_inicio')
    clases_reservadas_ids = Reserva.objects.filter(user=request.user, estado=EstadoReserva.ACTIVA).values_list('clase_programada_id', flat=True)
    # TURNOS
    turnos = Turno.objects.filter(activo=True).select_related('actividad').prefetch_related(
        Prefetch('clase_set', queryset=Clase.objects.filter(activo=True).order_by('dia', 'hora_inicio').prefetch_related(
            Prefetch('claseprogramada_set', queryset=ClaseProgramada.objects.filter(fecha__gte=hoy).order_by('fecha'))
        ))
    )
    for turno in turnos:
        turno.usuario_inscripto = turno.esta_inscripto(request.user)

    actividades_filtro = Actividad.objects.all().order_by('nombre')

    inscripciones_ids = Inscripcion.objects.filter(
        user=request.user,
        estado='ACTIVA'
    ).values_list('turno_id', flat=True)

    return render(request, 'reservas_disponibles.html', {
        'clases_programadas': clases_programadas,
        'clases_reservadas_ids': list(clases_reservadas_ids),
        'turnos': turnos,
        'inscripciones_ids': list(inscripciones_ids),
        'actividades_filtro': actividades_filtro
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
            messages.success(request, f'¡Excelente! Tu reserva para el {clase_programada.clase.get_dia_display()} a las {clase_programada.clase.hora_inicio} hs ha sido confirmada.')
            return redirect('reservas_disponibles')
    else:
        form = ReservaForm(user=request.user, clase_programada=clase_programada)

    return render(request, 'reservas/reserva_confirm.html', {'form': form, 'clase_programada': clase_programada})

@login_required
def reserva_list(request):
    hoy = timezone.localdate()
    reservas = Reserva.objects.filter(user=request.user).select_related('clase_programada__clase__turno__actividad').order_by('-clase_programada__fecha', 'clase_programada__clase__hora_inicio')

    inscripciones = Inscripcion.objects.filter(user=request.user)
    return render(request, 'reservas/reserva_list.html', {
        'reservas': reservas, 
        'inscripciones': inscripciones
    })

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
def inscripcion_confirm(request, turno_pk):
    turno = get_object_or_404(Turno, pk=turno_pk, activo=True)
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
            messages.success(request, f'¡Genial! Te inscribiste con éxito al turno {turno.nombre} de {turno.actividad.nombre}.')
            return redirect('reservas_disponibles')
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

@login_required
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
        estado=EstadoReserva.ACTIVA
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
        reserva.estado = EstadoReserva.PRESENTE
        reserva.asistio = True
        reserva.metodo_asistencia = 'QR'
        reserva.save()

        messages.success(request, f"Asistencia confirmada para {reserva.user.username}.")
        return redirect("escanear_qr")

    return render(request, "confirmar_asistencia.html", {"reserva": reserva})