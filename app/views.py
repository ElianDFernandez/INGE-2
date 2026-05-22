from django.shortcuts import render, redirect
from .forms import RegistroForm, PerfilForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from actividades.models import Actividad
from django.utils import timezone

# Create your views here.
def test(request):
    return HttpResponse("<h1>Hola Mundo!</h1>")

def bienvenida(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'app/landing.html')

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Cuenta creada con éxito! Ya podés iniciar sesión.')
            return redirect('login')
    else:
        form = RegistroForm()
        
    return render(request, 'app/registro.html', {'form': form})

@login_required
def home(request):
    return render(request, 'app/home.html')

@login_required
def perfil(request):
    if request.method == 'POST' and request.POST.get('action') == 'save':
        formulario = PerfilForm(request.POST, instance=request.user)
        if formulario.is_valid():
            usuario_actualizado = formulario.save()
            if formulario.cleaned_data.get('new_password'):
                update_session_auth_hash(request, usuario_actualizado)
            messages.success(request, '¡Tu perfil se actualizó correctamente!')
            return redirect('perfil')
        else:
            for campo, lista_de_errores in formulario.errors.items():
                for error in lista_de_errores:
                    messages.error(request, error)

    return render(request, 'app/perfil.html')

def home_view(request):
    # Trae todas las actividades de la base de datos
    actividades_reales = Actividad.objects.all() 
    
    # Se la pasamos al HTML
    return render(request, 'app/home.html', {
        'actividades': actividades_reales
    })

@login_required
def mis_inscripciones(request):
    return render(request, 'app/mis_inscripciones.html', {
        'turnos': [],
        'reservas': []
    })
