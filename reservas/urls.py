from django.urls import path
from .views import (reserva_list, reserva_confirm, reserva_cancel, reservas_disponibles,inscripcion_confirm, inscripcion_cancel)

urlpatterns = [
    # Panel de Mis Reservas
    path('', reserva_list, name='reserva_list'),
    
    # Reservas Disponibles
    path('disponibles/', reservas_disponibles, name='reservas_disponibles'),  
    
    # Acciones de Clases
    path('confirmar_reserva_clase/<int:clase_programada_pk>/', reserva_confirm, name='reserva_confirm'),
    path('cancelar_reserva_clase/<int:reserva_pk>/', reserva_cancel, name='reserva_cancel'),

    # Acciones de Turnos
    path('confirmar_inscripcion/<int:turno_pk>/', inscripcion_confirm, name='inscripcion_confirm'),
    path('cancelar_inscripcion/<int:inscripcion_pk>/', inscripcion_cancel, name='inscripcion_cancel'),
]