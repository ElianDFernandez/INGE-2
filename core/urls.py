from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('actividades/', include('actividades.urls')), 
    path('turnos/', include('turnos.urls')),
    path('empleados/', include('empleados.urls')),
    path('reservas/', include('reservas.urls')),
    path('socios/', include('socios.urls')),

    # App principal
    path('', include('app.urls')),
]
