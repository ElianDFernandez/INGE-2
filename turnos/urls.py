from django.urls import path
from .views import create_turno, TurnoListView, TurnoDeleteView, TurnoUpdateView

urlpatterns = [
    path('', TurnoListView.as_view(), name='turno_list'),
    path('nuevo_turno/', create_turno, name='turno_create'),
    path('turno/<int:pk>/editar/', TurnoUpdateView.as_view(), name='turno_edit'),
    path('turno/<int:pk>/eliminar/', TurnoDeleteView.as_view(), name='turno_delete'),
]