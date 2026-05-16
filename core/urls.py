from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Actividades
    path('actividades/', include('actividades.urls')), 
    
    # Empleados
    path('empleados/', include('empleados.urls')),

    # App principal
    path('', include('app.urls')),
]
