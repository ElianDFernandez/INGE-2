from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.http import HttpResponse
from .models import Clase, Turno
from .forms import TurnoForm, ClaseForm
from empleados.models import EmpleadoActividad

# Esta clase verifica que el usuario sea empleado (is_staff) o administrador (is_superuser)
class EmpleadoRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and (self.request.user.is_staff or self.request.user.is_superuser)


class TurnoActividadRequiredMixin(EmpleadoRequiredMixin):
    def test_func(self):
        if not super().test_func():
            return False
        user = self.request.user
        if user.is_superuser:
            return True
        turno = self.get_object()
        return EmpleadoActividad.objects.filter(empleado=user, actividad=turno.actividad).exists()

def placeholder(request):
    return HttpResponse("Página en construcción")

# Crea al turno con su clase asociada
def create_turno(request):
    if request.method == 'POST':
        turno_form = TurnoForm(request.POST)
       
        actividad = None
        if(turno_form.is_valid()):
            actividad = turno_form.cleaned_data['actividad']

        clase_form = ClaseForm(request.POST, actividad=actividad)

        if (turno_form.is_valid() and clase_form.is_valid()):
            turno = turno_form.save()
            clase = clase_form.save(commit=False)

            clase.turno = turno
            clase.save()

            return redirect('turno_list')
    else:
        turno_form = TurnoForm()
        clase_form = ClaseForm()

    return render(request, 'create_turno.html', {
        'turno_form': turno_form,
        'clase_form': clase_form
    })

class TurnoListView(EmpleadoRequiredMixin, ListView):
    model = Turno
    template_name = "turnos/turno_list.html"
    context_object_name = "turnos"

    def get_queryset(self):
        return super().get_queryset().select_related("actividad")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["actividades_asignadas_ids"] = set(
            EmpleadoActividad.objects.filter(empleado=self.request.user)
            .values_list("actividad_id", flat=True)
        )
        return context

class TurnoUpdateView(TurnoActividadRequiredMixin, UpdateView):
    model = Turno
    form_class = TurnoForm
    template_name = 'turnos/turno_edit.html'
    success_url = reverse_lazy('turno_list')

class TurnoDeleteView(TurnoActividadRequiredMixin, DeleteView):
    model = Turno
    template_name = 'turnos/turno_confirm_delete.html'
    success_url = reverse_lazy('turno_list')

class ClaseCreateView(EmpleadoRequiredMixin, CreateView):
    model = Clase
    form_class = ClaseForm
    template_name = 'clases/clase_form.html'
    success_url = reverse_lazy('turno_list')

    def form_valid(self, form):
            turno = get_object_or_404(
                Turno,
                pk=self.kwargs['turno_pk']
            )

            form.instance.turno = turno
            return super().form_valid(form)


class ClaseUpdateView(EmpleadoRequiredMixin, UpdateView):
    model = Clase
    form_class = ClaseForm
    template_name = 'clases/clase_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['actividad'] = self.object.turno.actividad
        return kwargs

    def get_success_url(self):
        return reverse_lazy(
            'turno_edit',
            kwargs={
                'pk': self.object.turno.pk
            }
        )

class ClaseDeleteView(EmpleadoRequiredMixin, DeleteView):
    model = Clase
    template_name = 'clases/clase_confirm_delete.html'
    success_url = reverse_lazy('turno_list')
    
    def get_success_url(self):
        return reverse_lazy(
            'turno_edit',
            kwargs={
                'pk': self.object.turno.pk
            }
        )