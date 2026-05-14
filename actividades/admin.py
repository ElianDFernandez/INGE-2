from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Actividad, Turno

@admin.register(Actividad)
class ActividadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'cupo_maximo')

@admin.register(Turno)
class TurnoAdmin(admin.ModelAdmin):
    list_display = ('actividad', 'dia_semana', 'horario_inicio', 'cupo_disponible')
    list_filter = ('dia_semana', 'actividad')
