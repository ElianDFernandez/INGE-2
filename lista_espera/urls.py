from django.urls import path
from . import views

urlpatterns = [
    path('<int:lista_espera_id>/confirmar/', views.confirmar_desde_email, name='confirmar_desde_email'),
    path('<int:lista_espera_id>/pago-exitoso/<int:reserva_id>/', views.pago_exitoso_lista_espera, name='pago_exitoso_lista_espera'),
    path('<int:lista_espera_id>/pago-fallido/<int:reserva_id>/', views.pago_fallido_lista_espera, name='pago_fallido_lista_espera'),
]