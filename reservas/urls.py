from django.urls import path
from .views import clases_disponibles, reserva_confirm

urlpatterns = [
    path('clases_disponibles/', clases_disponibles, name='clases_disponibles'),
    path('confirmar/<int:clase_programada_pk>/', reserva_confirm, name='reserva_confirm'),
]