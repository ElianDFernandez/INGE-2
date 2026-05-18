from django.urls import path
from .views import clases_disponibles, reserva_list, reserva_confirm, reserva_cancel

urlpatterns = [
    path('', reserva_list, name='reserva_list'),
    path('clases_disponibles/', clases_disponibles, name='clases_disponibles'),  
    path('confirmar/<int:clase_programada_pk>/', reserva_confirm, name='reserva_confirm'),
    path('cancelar/<int:reserva_pk>/', reserva_cancel, name='reserva_cancel'),
]