from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib import messages
from reservas.models import EstadoReserva, Reserva, Inscripcion
from socios.models import Socio

# 1. LISTADO GENERAL DE SOCIOS + BUSCADOR
@login_required
@staff_member_required(login_url='home')
def socio_list(request):
    q = request.GET.get('q', '')
    
    # Traigo los usuarios comunes (Socios), excluyendo staff y admins
    socios = User.objects.filter(is_staff=False, is_superuser=False).order_by('username')
    
    # Si se usa el buscador, filtra por nombre de usuario o email
    if q:
        socios = socios.filter(username__icontains=q) | socios.filter(email__icontains=q)
        
    return render(request, 'socios/socio_list.html', {
        'socios': socios,
        'q': q
    })

# 2. VER RESERVAS DE UN SOCIO ESPECÍFICO
@login_required
@staff_member_required(login_url='home')
def socio_reservas(request, socio_id):
    # Traigo el historial de reservas de este usuario particular
    socio = get_object_or_404(User, id=socio_id)
    reservas = Reserva.objects.filter(user=socio).select_related(
        'clase_programada__clase__turno__actividad'
    ).order_by('clase_programada__fecha', 'clase_programada__clase__hora_inicio').exclude(estado='INICIADA')
    inscripciones = Inscripcion.objects.filter(user=socio).select_related(
        'turno__actividad'
    ).order_by('-fecha_alta').exclude(estado='INICIADA')
    return render(request, 'socios/socio_reservas.html', {
        'socio': socio,
        'reservas': reservas,
        'inscripciones': inscripciones,
    })

# 3. ACCIÓN: REGISTRAR ASISTENCIA MANUAL
@login_required
@staff_member_required(login_url='home')
def registrar_asistencia(request, reserva_id):
    if request.method == 'POST':
        reserva = get_object_or_404(Reserva, id=reserva_id)
        reserva.asistio = True
        reserva.metodo_asistencia = 'MANUAL'
        reserva.save()
        messages.success(request, f"Asistencia confirmada para {reserva.user.username}.")
    return redirect(request.META.get('HTTP_REFERER', 'socio_list'))

# 4. ACCIÓN: REGISTRAR PAGO MANUAL
@login_required
@staff_member_required(login_url='home')
def registrar_pago(request, reserva_id):
    if request.method == 'POST':
        reserva = get_object_or_404(Reserva, id=reserva_id)
        
        # Guardamos los datos del pago
        reserva.pago_confirmado = True 
        reserva.metodo_pago = 'MANUAL'
        
        reserva.estado = 'ACTIVA' 
        # -----------------------------------
        
        reserva.save()
        messages.success(request, f"Pago registrado con éxito para la clase de {reserva.user.username}.")
    return redirect(request.META.get('HTTP_REFERER', 'socio_list'))

@login_required
@staff_member_required(login_url='home')
def registrar_devolucion(request, reserva_id):
    if request.method == 'POST':
        reserva = get_object_or_404(Reserva, id=reserva_id)
        
        # Marcamos que ya se le devolvió la seña manualmente
        reserva.sena_devuelta = True
        reserva.save()
        
        # Mensaje aclaratorio de que es manual
        messages.success(request, f"Reembolso registrado para {reserva.user.username}.")
        
    return redirect(request.META.get('HTTP_REFERER', 'socio_list'))

@login_required
@staff_member_required(login_url='home')
def registrar_pago_inscripcion(request, inscripcion_id):
    if request.method == 'POST':
        inscripcion = get_object_or_404(Inscripcion, id=inscripcion_id)
        inscripcion.estado = 'ACTIVA'
        inscripcion.mp_payment_id = 'MANUAL'
        inscripcion.save()
        # Crear las reservas de las clases del turno
        inscripcion.reservar_clases_programadas()
        messages.success(request, f"Pago de turno registrado con éxito para {inscripcion.user.username}.")
    return redirect(request.META.get('HTTP_REFERER', 'socio_list'))

@login_required
def socio_mis_vales(request):
    socio = request.user
    hoy = timezone.localdate()
    vales_disponibles = socio.vales.filter(
        usado=False, fecha_vencimiento__gte=hoy
    ).select_related('actividad').order_by('actividad__nombre', 'fecha_vencimiento')

    vales_usados = socio.vales.filter(usado=True).select_related(
        'actividad'
    ).order_by('-fecha_uso')

    vales_vencidos = socio.vales.filter(
        usado=False, fecha_vencimiento__lt=hoy
    ).select_related('actividad').order_by('-fecha_vencimiento')

    return render(request, 'socios/socio_mis_vales.html', {
        'socio': socio,
        'vales_disponibles': vales_disponibles,
        'vales_usados': vales_usados,
        'vales_vencidos': vales_vencidos,
    })