from django.urls import path
from . import views

urlpatterns = [
    path('', views.socio_list, name='socio_list'),
    path('<int:socio_id>/reservas/', views.socio_reservas, name='socio_reservas'),
    path('reserva/<int:reserva_id>/asistencia/', views.registrar_asistencia, name='registrar_asistencia'),
    path('reserva/<int:reserva_id>/pago/', views.registrar_pago, name='registrar_pago'),
    path('reserva/<int:reserva_id>/devolucion/', views.registrar_devolucion, name='registrar_devolucion'),
    path('mis-creditos/', views.socio_mis_creditos, name='socio_mis_creditos'),
]