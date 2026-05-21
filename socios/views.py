from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib import messages
from reservas.models import Reserva

# Función de validación de permisos
def es_empleado_o_admin(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)

# 1. LISTADO GENERAL DE SOCIOS + BUSCADOR
@login_required
@user_passes_test(es_empleado_o_admin, login_url='home')
def socio_list(request):
    q = request.GET.get('q', '')
    
    # Traigo los usuarios comunes (Socios), excluyendo staff y admins
    socios = User.objects.filter(is_staff=False, is_superuser=False).order_by('username')
    
    # Si se usa el buscador, filtramos por nombre de usuario o email
    if q:
        socios = socios.filter(username__icontains=q) | socios.filter(email__icontains=q)
        
    return render(request, 'socios/socio_list.html', {
        'socios': socios,
        'q': q
    })

@login_required
@user_passes_test(es_empleado_o_admin, login_url='home')
def socio_reservas(request, socio_id):
    # Por ahora solo traemos al socio, después le agregamos las reservas de verdad
    socio = get_object_or_404(User, id=socio_id)
    return render(request, 'socios/socio_reservas.html', {'socio': socio})

