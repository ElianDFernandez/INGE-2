from django.urls import path
from .views import clases_disponibles, reserva_list, reserva_confirm, reserva_cancel, turnos_disponibles, inscripcion_confirm, inscripcion_cancel

urlpatterns = [
    path('', reserva_list, name='reserva_list'),
    path('clases_disponibles/', clases_disponibles, name='clases_disponibles'),  
    path('confirmar_reserva_clase/<int:clase_programada_pk>/', reserva_confirm, name='reserva_confirm'),
    path('cancelar_reserva_clase/<int:reserva_pk>/', reserva_cancel, name='reserva_cancel'),

    path('turnos_disponibles/', turnos_disponibles, name='turnos_disponibles'),
    path('confirmar_inscripcion/<int:turno_pk>/', inscripcion_confirm, name='inscripcion_confirm'),
    path('cancelar_inscripcion/<int:inscripcion_pk>/', inscripcion_cancel, name='inscripcion_cancel'),
]