from django.urls import path
from . import views

urlpatterns = [
    path('', views.socio_list, name='socio_list'),
    path('<int:socio_id>/reservas/', views.socio_reservas, name='socio_reservas'),
]