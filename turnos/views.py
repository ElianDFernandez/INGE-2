from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.http import HttpResponse
from .models import Clase, Turno
from .forms import TurnoForm, ClaseForm

# Esta clase verifica que el usuario sea empleado (is_staff) o administrador (is_superuser)
class EmpleadoRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and (self.request.user.is_staff or self.request.user.is_superuser)

def placeholder(request):
    return HttpResponse("Página en construcción")

# Crea al turno con su clase asociada
def create_turno(request):
    if request.method == 'POST':
        turno_form = TurnoForm(request.POST)
        clase_form = ClaseForm(request.POST)

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
    template_name = 'turnos/turno_list.html'
    context_object_name = 'turnos'

class TurnoUpdateView(EmpleadoRequiredMixin, UpdateView):
    model = Turno
    form_class = TurnoForm
    template_name = 'turnos/turno_edit.html'
    success_url = reverse_lazy('turno_list')

class TurnoDeleteView(EmpleadoRequiredMixin, DeleteView):
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