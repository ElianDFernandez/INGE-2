from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib import messages
from reservas.models import EstadoReserva, Reserva
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
    reservas = Reserva.objects.filter(user=socio).order_by('clase_programada__fecha', 'clase_programada__clase__hora_inicio')
    return render(request, 'socios/socio_reservas.html', {
        'socio': socio,
        'reservas': reservas})

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
        reserva.pago_confirmado = True 
        reserva.metodo_pago = 'MANUAL'
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
        messages.success(request, f"Pago devuelto manualmente a {reserva.user.username}. (La carga automática de créditos se implementará en el próximo sprint).")
        
    return redirect(request.META.get('HTTP_REFERER', 'socio_list'))

@login_required
def socio_mis_creditos(request):
    socio = request.user 
    return render(request, 'socios/socio_mis_creditos.html', {
        'socio': socio
    })