from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.http import HttpResponse
from .models import Clase, Turno
from .forms import TurnoForm, ClaseForm
from empleados.models import EmpleadoActividad
from django.db.models import Prefetch

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

# Crea al turno con su clase asociada, y genera las clases de este mes
def create_turno(request):
    clase_forms = []
    cupo_global = ''
    if request.method == 'POST':
        turno_form = TurnoForm(request.POST, user=request.user)
        
        if turno_form.is_valid():
            actividad = turno_form.cleaned_data['actividad']
            
            dias = request.POST.getlist('dia')
            espacios = request.POST.getlist('espacio')
            horas_inicio = request.POST.getlist('hora_inicio')
            horas_fin = request.POST.getlist('hora_fin')
            costos = request.POST.getlist('costo')            
            cupo_global = request.POST.get('cupo_maximo')
            
            clases_validas = []
            hay_errores = False
            
            # 3. Recorremos y armamos cada clase
            for i in range(len(dias)):
                clase_data = {
                    'dia': dias[i],
                    'espacio': espacios[i],
                    'hora_inicio': horas_inicio[i],
                    'hora_fin': horas_fin[i],
                    'costo': costos[i],
                    'cupo_maximo': cupo_global  # Mismo cupo para todas las clases del turno
                }
                
                clase_form = ClaseForm(clase_data, actividad=actividad)
                clase_forms.append(clase_form)
                
                if clase_form.is_valid():
                    clases_validas.append(clase_form.save(commit=False))
                else:
                    hay_errores = True
                    for error in clase_form.non_field_errors():
                        messages.error(request, f"Error en la Clase {i+1}: {error}")
            
            if not hay_errores and clases_validas:
                turno = turno_form.save()
                for clase in clases_validas:
                    clase.turno = turno
                    clase.save()
                    
                turno.generar_clases_programadas()
                return redirect('turno_list')
        else:
            actividad = None
            dias = request.POST.getlist('dia')
            espacios = request.POST.getlist('espacio')
            horas_inicio = request.POST.getlist('hora_inicio')
            horas_fin = request.POST.getlist('hora_fin')
            costos = request.POST.getlist('costo')
            cupo_global = request.POST.get('cupo_maximo')

            for i in range(len(dias)):
                clase_data = {
                    'dia': dias[i],
                    'espacio': espacios[i],
                    'hora_inicio': horas_inicio[i],
                    'hora_fin': horas_fin[i],
                    'costo': costos[i],
                    'cupo_maximo': cupo_global
                }
                clase_forms.append(ClaseForm(clase_data, actividad=actividad))
    else:
        turno_form = TurnoForm(user=request.user)
        clase_forms = [ClaseForm()]
        cupo_global = ''

    return render(request, 'create_turno.html', {
        'turno_form': turno_form,
        'clase_forms': clase_forms,
        'cupo_maximo': cupo_global
    })
class TurnoListView(EmpleadoRequiredMixin, ListView):
    model = Turno
    template_name = "turnos/turno_list.html"
    context_object_name = "turnos"

    def get_queryset(self):
        clases_activas = Prefetch(
            "clase_set", 
            queryset=Clase.objects.filter(activo=True)
        )

        return (
            super().get_queryset()
            .select_related("actividad")
            .prefetch_related(clases_activas)
            .filter(activo=True)
            .order_by("actividad__nombre", "nombre")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["actividades_asignadas_ids"] = set(
            EmpleadoActividad.objects.filter(empleado=self.request.user).values_list("actividad_id", flat=True)
        )
        context["turnos_con_reservas_ids"] = set(
            Turno.objects.filter(clase__claseprogramada__reserva__isnull=False).exclude(clase__claseprogramada__reserva__estado='CANCELADA').values_list("id", flat=True).distinct()
        )
        return context
class TurnoUpdateView(TurnoActividadRequiredMixin, UpdateView):
    model = Turno
    form_class = TurnoForm
    template_name = 'turnos/turno_edit.html'
    success_url = reverse_lazy('turno_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        clases = self.object.clase_set.filter(activo=True)
        formularios_clases = [ClaseForm(instance=clase) for clase in clases]
        context['clase_forms'] = formularios_clases
        context['clase_form_molde'] = ClaseForm() # Molde vacío para el JavaScript
        # Enviamos el cupo general (tomando el de la primera clase)
        context['cupo_maximo'] = clases.first().cupo_maximo if clases.exists() else ''
        context['puede_modificar'] = [clase.puede_modificar() for clase in clases] # Lista de booleanos para cada clase
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        turno_form = self.get_form()
        if turno_form.is_valid():
            clase_ids = request.POST.getlist('clase_id')
            dias = request.POST.getlist('dia')
            espacios = request.POST.getlist('espacio')
            horas_inicio = request.POST.getlist('hora_inicio')
            horas_fin = request.POST.getlist('hora_fin')
            costos = request.POST.getlist('costo')
            cupo_global = request.POST.get('cupo_maximo')
            cupo_int = int(cupo_global) if cupo_global and cupo_global.isdigit() else 0
            reservas_maximas = self.object.max_reservas_actuales()
            if cupo_int < reservas_maximas:
                messages.error(request, f"No puedes reducir el cupo a {cupo_int}. Ya existen clases programadas con reservas activas.")
                return self.form_invalid(turno_form)
            ids_recibidos = [int(i) for i in clase_ids if i.isdigit()]
            # CANCELACION DE CLASES EXISTENTES NO RECIBIDAS
            for clase in self.object.clase_set.filter(activo=True):
                if clase.id not in ids_recibidos:
                    clase.cancelacion_por_modificacion()
            actividad = turno_form.cleaned_data['actividad']
            hay_errores = False
            
            for i in range(len(dias)):
                clase_data = {
                    'dia': dias[i], 'espacio': espacios[i],
                    'hora_inicio': horas_inicio[i], 'hora_fin': horas_fin[i],
                    'costo': costos[i], 'cupo_maximo': cupo_global
                }
                c_id = clase_ids[i] if i < len(clase_ids) else ""
                if c_id.isdigit():
                    instancia_clase = Clase.objects.get(id=c_id)
                    clase_form = ClaseForm(clase_data, instance=instancia_clase, actividad=actividad)
                else: 
                    clase_form = ClaseForm(clase_data, actividad=actividad) 
                if clase_form.is_valid():
                    if c_id.isdigit():
                        # ACTUALIZACIÓN DE CLASE EXISTENTE
                        if clase_form.has_changed():
                            instancia_clase.reemplazar_por_modificacion(clase_form.cleaned_data)
                    else:
                        # CREACIÓN DE CLASE NUEVA
                        clase = clase_form.save(commit=False)
                        clase.turno = self.object
                        clase.save()
                else:
                    hay_errores = True
                    for error in clase_form.non_field_errors():
                        messages.error(request, f"Error en horario {i+1}: {error}")

            if not hay_errores:
                turno_form.save()
                self.object.generar_clases_programadas()
                messages.success(request, 'Turno actualizado correctamente. Las clases modificadas cancelaron sus reservas antiguas.')
                return redirect(self.success_url)
            else:
                return self.form_invalid(turno_form)
        else:
            return self.form_invalid(turno_form)

# Soft Delete, turno y clases asociadas se desactivan (pero siguen estando en la DB)
class TurnoDeleteView(TurnoActividadRequiredMixin, DeleteView):
    model = Turno
    template_name = 'turnos/turno_confirm_delete.html'
    success_url = reverse_lazy('turno_list')

    def get_queryset(self):
        return Turno.objects.filter(activo=True)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.tiene_reservas():
            messages.error(
                request,
                f'No se puede eliminar el turno "{self.object.nombre}" porque tiene reservas activas asociadas.'
            )
            return redirect(self.success_url)
        
        self.object.desactivar()
        return redirect(self.success_url)

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

    def get_queryset(self):
        return Clase.objects.filter(activo=True)

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

    def get_queryset(self):
        return Clase.objects.filter(activo=True)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.tiene_reservas():
            messages.error(
                request,
                'No se puede eliminar la clase porque tiene reservas asociadas.'
            )
            return redirect(self.get_success_url())
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tiene_reservas'] = self.object.tiene_reservas()
        return context
    
    def get_success_url(self):
        return reverse_lazy(
            'turno_edit',
            kwargs={
                'pk': self.object.turno.pk
            }
        )