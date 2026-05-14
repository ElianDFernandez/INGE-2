from django.urls import path
from .views import ActividadListView, ActividadCreateView

urlpatterns = [
    path('', ActividadListView.as_view(), name='actividades_list'),
    path('nueva/', ActividadCreateView.as_view(), name='actividad_create'),
]