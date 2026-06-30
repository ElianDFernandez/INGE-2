from django.urls import path
from .views import (reserva_list, reserva_confirm, reserva_cancel, reservas_disponibles,inscripcion_confirm, inscripcion_cancel, pago_exitoso, pago_fallido, pagar_restante)

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

    # Acciones de MercadoPago
    path('reserva/<int:reserva_id>/pago-exitoso/', pago_exitoso, name='pago_exitoso'),
    path('reserva/<int:reserva_id>/pago-fallido/', pago_fallido, name='pago_fallido'),
    path('reserva/<int:reserva_id>/pagar-restante/', pagar_restante, name='pagar_restante'),
]