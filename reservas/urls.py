from django.urls import path
from .views import (reserva_list, reserva_confirm, reserva_cancel, reservas_disponibles,inscripcion_confirm, inscripcion_cancel)
from lista_espera import views as lista_espera_views
from django.urls import path, include
from .views import (reservas_disponibles, reserva_list, reserva_confirm, reserva_cancel, reserva_qr, reserva_qr_image, escanear_qr, confirmar_asistencia, inscripcion_confirm, inscripcion_cancel, inscripcion_pago_exitoso, inscripcion_pago_fallido, pago_exitoso, pago_fallido, pagar_restante, simular_reembolso, renovar_inscripcion_confirm, renovar_pago_exitoso, renovar_pago_fallido)

urlpatterns = [
    # Panel de Mis Reservas
    path('', reserva_list, name='reserva_list'),
    
    # Reservas Disponibles
    path('disponibles/', reservas_disponibles, name='reservas_disponibles'),  
    
    # Acciones de Clases
    path('confirmar_reserva_clase/<int:clase_programada_pk>/', reserva_confirm, name='reserva_confirm'),
    path('cancelar_reserva_clase/<int:reserva_pk>/', reserva_cancel, name='reserva_cancel'),
    path('qr_asistencia/<int:reserva_pk>/', reserva_qr, name='reserva_qr'),
    # lo necesito para mostrar la imagen del qr
    path('qr_asistencia/<int:reserva_pk>/imagen/', reserva_qr_image, name='reserva_qr_image'),

    # solo visible para admin y empleados
    path('escanear_qr/', escanear_qr, name='escanear_qr'),
    path('confirmar_asistencia/<str:qr_token>/', confirmar_asistencia, name='confirmar_asistencia'),

    # Acciones de Turnos
    path('confirmar_inscripcion/<int:turno_pk>/', inscripcion_confirm, name='inscripcion_confirm'),
    path('cancelar_inscripcion/<int:inscripcion_pk>/', inscripcion_cancel, name='inscripcion_cancel'), 

    #Acciones de lista de espera 
    path('<int:clase_programada_pk>/lista-espera/inscribirse/', lista_espera_views.inscribirse_lista_espera, name='inscribirse_lista_espera'),
    path('<int:clase_programada_pk>/lista-espera/cancelar/', lista_espera_views.cancelar_lista_espera, name='cancelar_lista_espera'),

    path('', include('lista_espera.urls')), 
    path('cancelar_inscripcion/<int:inscripcion_pk>/', inscripcion_cancel, name='inscripcion_cancel'),

    # Acciones de MercadoPago
    path('reserva/<int:reserva_id>/pago-exitoso/', pago_exitoso, name='pago_exitoso'),
    path('reserva/<int:reserva_id>/pago-fallido/', pago_fallido, name='pago_fallido'),
    path('reserva/<int:reserva_id>/pagar-restante/', pagar_restante, name='pagar_restante'),

    # Pago de Inscripciones
    path('inscripcion/<int:inscripcion_id>/pago-exitoso/', inscripcion_pago_exitoso, name='inscripcion_pago_exitoso'),
    path('inscripcion/<int:inscripcion_id>/pago-fallido/', inscripcion_pago_fallido, name='inscripcion_pago_fallido'),

    # Renovación de Turno (socio ya inscripto)
    path('renovar_turno/<int:turno_pk>/', renovar_inscripcion_confirm, name='renovar_inscripcion_confirm'),
    path('renovacion/<int:inscripcion_id>/pago-exitoso/', renovar_pago_exitoso, name='renovar_pago_exitoso'),
    path('renovacion/<int:inscripcion_id>/pago-fallido/', renovar_pago_fallido, name='renovar_pago_fallido'),

    # Simulación de reembolso
    path('reembolso/<int:reserva_pk>/', simular_reembolso, name='simular_reembolso'),
]