from django.shortcuts import render, redirect
from .forms import RegistroForm 
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

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