from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Actividad
from .forms import ActividadForm

# Esta clase verifica que el usuario sea empleado (is_staff) o administrador (is_superuser)
class EmpleadoRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and (self.request.user.is_staff or self.request.user.is_superuser)

class ActividadListView(EmpleadoRequiredMixin, ListView):
    model = Actividad
    template_name = 'actividades/actividad_list.html'
    context_object_name = 'actividades'

class ActividadCreateView(EmpleadoRequiredMixin, CreateView):
    model = Actividad
    form_class = ActividadForm
    template_name = 'actividades/actividad_form.html'
    success_url = reverse_lazy('actividades_list')


class ActividadUpdateView(EmpleadoRequiredMixin, UpdateView):
    model = Actividad
    form_class = ActividadForm
    template_name = 'actividades/actividad_form.html' 
    success_url = reverse_lazy('actividades_list')

class ActividadDeleteView(EmpleadoRequiredMixin, DeleteView):
    model = Actividad
    template_name = 'actividades/actividad_confirm_delete.html'
    success_url = reverse_lazy('actividades_list')

    def _tiene_reservas(self):
        return self.object.tiene_reservas()

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self._tiene_reservas():
            messages.error(
                request,
                f'No se puede eliminar la actividad "{self.object.nombre}" porque tiene turnos con reservas asociadas.'
            )
            return redirect(self.success_url)
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tiene_reservas'] = self.object.tiene_reservas()
        return context