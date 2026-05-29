from django.shortcuts import render, redirect
from .forms import RegistroForm, PerfilForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import update_session_auth_hash
import json

from empleados.models import Empleado
from socios.models import Socio

# Create your views here.
def test(request):
    return HttpResponse("<h1>Hola Mundo!</h1>")


def pwa_manifest(request):
        manifest = {
                "name": "Centro de Actividades Deportivas",
                "short_name": "CAD",
                "description": "Sistema de gestión para centros de actividades",
                "start_url": "/",
                "scope": "/",
                "display": "standalone",
                "background_color": "#F9F9F9",
                "theme_color": "#004383",
                "icons": [
                        {
                                "src": "/static/app/pwa-icon.svg",
                                "sizes": "512x512",
                                "type": "image/svg+xml",
                                "purpose": "any maskable",
                        }
                ],
        }
        response = HttpResponse(json.dumps(manifest), content_type='application/manifest+json')
        response['Cache-Control'] = 'no-cache'
        return response


def pwa_service_worker(request):
        script = """
const CACHE_NAME = 'centro-gestion-pwa-v1';
const APP_SHELL = [
    '/',
    '/login/',
    '/registro/',
    '/manifest.webmanifest',
    '/static/icon.svg',
    '/static/logo.svg',
    '/static/app/pwa-icon.svg',
];

const OFFLINE_HTML = `
<!doctype html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Sin conexión</title>
    <style>
        body {
            margin: 0;
            min-height: 100vh;
            display: grid;
            place-items: center;
            font-family: Arial, sans-serif;
            background: #F9F9F9;
            color: #121212;
        }
        .card {
            max-width: 28rem;
            padding: 2rem;
            margin: 1rem;
            border-radius: 1rem;
            background: #fff;
            box-shadow: 0 16px 40px rgba(0, 67, 131, 0.12);
            text-align: center;
        }
        h1 {
            margin-top: 0;
            color: #004383;
        }
        p {
            line-height: 1.5;
            color: #4b5563;
        }
    </style>
</head>
<body>
    <div class="card">
        <h1>Estás sin conexión</h1>
        <p>La aplicación está instalada, pero en este momento no se puede cargar contenido nuevo. Volvé a intentarlo cuando recuperes internet.</p>
    </div>
</body>
</html>
`;

self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME).then(cache => cache.addAll(APP_SHELL)).then(() => self.skipWaiting())
    );
});

self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(keys => Promise.all(
            keys.filter(key => key !== CACHE_NAME).map(key => caches.delete(key))
        )).then(() => self.clients.claim())
    );
});

self.addEventListener('fetch', event => {
    if (event.request.method !== 'GET') {
        return;
    }

    if (event.request.mode === 'navigate') {
        event.respondWith((async () => {
            try {
                const networkResponse = await fetch(event.request);
                const cache = await caches.open(CACHE_NAME);
                cache.put(event.request, networkResponse.clone());
                return networkResponse;
            } catch (error) {
                const cachedResponse = await caches.match(event.request, { ignoreSearch: true });
                if (cachedResponse) {
                    return cachedResponse;
                }

                const homeResponse = await caches.match('/');
                if (homeResponse) {
                    return homeResponse;
                }

                return new Response(OFFLINE_HTML, {
                    headers: { 'Content-Type': 'text/html; charset=utf-8' },
                });
            }
        })());
        return;
    }

    if (event.request.url.startsWith(self.location.origin)) {
        event.respondWith((async () => {
            const cachedResponse = await caches.match(event.request);
            if (cachedResponse) {
                return cachedResponse;
            }

            try {
                const networkResponse = await fetch(event.request);
                if (networkResponse && networkResponse.ok) {
                    const cache = await caches.open(CACHE_NAME);
                    cache.put(event.request, networkResponse.clone());
                }
                return networkResponse;
            } catch (error) {
                return caches.match('/static/app/pwa-icon.svg');
            }
        })());
    }
});
"""
        response = HttpResponse(script, content_type='application/javascript')
        response['Cache-Control'] = 'no-cache'
        response['Service-Worker-Allowed'] = '/'
        return response

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