from django.urls import path
from .views import ActividadListView, ActividadCreateView,ActividadUpdateView,ActividadDeleteView

urlpatterns = [
    path('', ActividadListView.as_view(), name='actividades_list'),
    path('nueva/', ActividadCreateView.as_view(), name='actividad_create'),
    path('<int:pk>/editar/', ActividadUpdateView.as_view(), name='actividad_edit'),
    path('<int:pk>/eliminar/', ActividadDeleteView.as_view(), name='actividad_delete'),
]