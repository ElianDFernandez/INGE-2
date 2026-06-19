from django.urls import path
from . import views

urlpatterns = [
    path('<int:lista_espera_id>/confirmar/', views.confirmar_desde_email, name='confirmar_desde_email'),
]