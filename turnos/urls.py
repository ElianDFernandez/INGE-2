from django.urls import path
from .views import TurnoListView, TurnoCreateView, TurnoDeleteView, placeholder

urlpatterns = [
    path('', TurnoListView.as_view(), name='turno_list'),
    path('nuevo/', TurnoCreateView.as_view(), name='turno_create'),
    path('<int:pk>/editar/', placeholder, name='turno_edit'),
    path('<int:pk>/eliminar/', TurnoDeleteView.as_view(), name='turno_delete'),
]