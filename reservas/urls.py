from django.urls import path
from .views import (reserva_list, reserva_confirm, reserva_cancel, reservas_disponibles,inscripcion_confirm, inscripcion_cancel)
from lista_espera import views as lista_espera_views
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

    #Acciones de lista de espera 
    path('<int:clase_programada_pk>/lista-espera/inscribirse/', lista_espera_views.inscribirse_lista_espera, name='inscribirse_lista_espera'),
    path('<int:clase_programada_pk>/lista-espera/cancelar/', lista_espera_views.cancelar_lista_espera, name='cancelar_lista_espera'),
       
]