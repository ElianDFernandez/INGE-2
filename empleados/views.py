from django.shortcuts import get_object_or_404, redirect
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from actividades.models import Actividad
from empleados.models import Empleado, EmpleadoActividad
from empleados.forms import EmpleadoCreateForm, EmpleadoUpdateForm

# Create your views here.

class EmpleadosListView(ListView):
    model = Empleado
    template_name = 'empleados/empleados_list.html'
    context_object_name = 'empleados'

    def get_queryset(self):
        return super().get_queryset().filter(is_superuser=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        actividades = list(Actividad.objects.all())
        empleados = list(context['empleados'])

        for empleado in empleados:
            empleado.actividades_ids = set(
                EmpleadoActividad.objects.filter(empleado=empleado)
                .values_list('actividad_id', flat=True)
            )

        context['actividades'] = actividades
        context['empleados'] = empleados
        return context


class EmpleadoCreateView(CreateView):
    model = Empleado
    form_class = EmpleadoCreateForm
    template_name = 'empleados/empleados_form.html'
    success_url = reverse_lazy('empleados_list')


class EmpleadoUpdateView(UpdateView):
    model = Empleado
    form_class = EmpleadoUpdateForm
    template_name = 'empleados/empleados_form.html'
    success_url = reverse_lazy('empleados_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.object.email:
            send_mail(
                subject="Actualizacion de cuenta de empleado",
                message=(
                    "Tu cuenta de empleado fue actualizada.\n"
                    "Si no realizaste este cambio, contacta al administrador."
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[self.object.email],
                fail_silently=True,
            )
        return response


class EmpleadoDeleteView(DeleteView):
    model = Empleado
    template_name = 'empleados/empleados_confirm_delete.html'
    success_url = reverse_lazy('empleados_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.email:
            send_mail(
                subject="Baja de cuenta de empleado",
                message=(
                    "Tu cuenta de empleado fue dada de baja.\n"
                    "Si crees que es un error, contacta al administrador."
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[self.object.email],
                fail_silently=True,
            )
        return super().delete(request, *args, **kwargs)


@require_POST
def gestionar_actividades(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    seleccionadas = set(map(int, request.POST.getlist('actividad_ids')))
    actuales = set(
        EmpleadoActividad.objects.filter(empleado=empleado)
        .values_list('actividad_id', flat=True)
    )

    agregar = seleccionadas - actuales
    quitar = actuales - seleccionadas

    if agregar:
        EmpleadoActividad.objects.bulk_create(
            [EmpleadoActividad(empleado=empleado, actividad_id=actividad_id) for actividad_id in agregar]
        )

    if quitar:
        EmpleadoActividad.objects.filter(empleado=empleado, actividad_id__in=quitar).delete()

    return redirect('empleados_list')

