from django.shortcuts import render, redirect
from .forms import RegistroForm, PerfilForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import update_session_auth_hash

from empleados.models import Empleado
from socios.models import Socio

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
    return render(request, 'app/home.html', contexto_home(request.user))

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

def contexto_home(usuario):
    socio = Socio.objects.filter(pk=usuario.pk).first()
    if socio:
        return socio.get_contexto_home()

    empleado = Empleado.objects.filter(pk=usuario.pk).first()
    if empleado:
        return empleado.get_contexto_home()

    return {}