from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 1. Rutas específicas primero: Todo lo que empiece con /actividades/ va para allá
    path('actividades/', include('actividades.urls')), 
    
    # 2. Ruta general al final: El resto (inicio, login, perfil) lo maneja la app principal
    path('', include('app.urls')),
]
