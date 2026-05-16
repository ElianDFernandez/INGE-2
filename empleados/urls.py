from django.urls import path
from .views import EmpleadosListView, EmpleadoCreateView, EmpleadoUpdateView, EmpleadoDeleteView, gestionar_actividades

urlpatterns = [
    path('', EmpleadosListView.as_view(), name='empleados_list'),
    path('nuevo/', EmpleadoCreateView.as_view(), name='empleados_create'),
    path('<int:pk>/editar/', EmpleadoUpdateView.as_view(), name='empleados_edit'),
    path('<int:pk>/eliminar/', EmpleadoDeleteView.as_view(), name='empleados_delete'),
    path('<int:pk>/actividades/', gestionar_actividades, name='empleados_actividades'),
]