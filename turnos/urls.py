from django.urls import path
from .views import create_turno, ClaseCreateView, ClaseDeleteView, ClaseUpdateView, TurnoListView, TurnoDeleteView, TurnoUpdateView

urlpatterns = [
    path('', TurnoListView.as_view(), name='turno_list'),
    path('nuevo_turno/', create_turno, name='turno_create'),
    path('turno/<int:pk>/editar/', TurnoUpdateView.as_view(), name='turno_edit'),
    path('turno/<int:pk>/eliminar/', TurnoDeleteView.as_view(), name='turno_delete'),
    path('turno/<int:turno_pk>/nueva_clase/', ClaseCreateView.as_view(), name='clase_create'),
    path('clase/<int:pk>/editar/', ClaseUpdateView.as_view(), name='clase_edit'),
    #path('clase/<int:pk>/eliminar/', ClaseDeleteView.as_view(), name='clase_delete'),
]