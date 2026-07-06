from django.shortcuts import redirect, render
from django.contrib import messages
from django.views.generic import ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Clase, Turno
from .forms import TurnoForm, ClaseForm
from empleados.models import EmpleadoActividad
from django.db.models import Count, Prefetch, Q
from django.utils import timezone
from calendar import Calendar
from datetime import datetime

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
    if request.method == 'POST':
        turno_form = TurnoForm(request.POST, user=request.user)
        cupo_global = request.POST.get('cupo_maximo')
        clase_forms = []
        if turno_form.is_valid():
            actividad = turno_form.cleaned_data['actividad']
            dias = request.POST.getlist('dia')
            espacios = request.POST.getlist('espacio')
            horas_inicio = request.POST.getlist('hora_inicio')
            horas_fin = request.POST.getlist('hora_fin')
            costos = request.POST.getlist('costo')
            cupo_int = int(cupo_global) if cupo_global and cupo_global.isdigit() else 0
            if cupo_int <= 0:
                messages.error(request, "El cupo máximo debe ser mayor a 0.")
                for i in range(len(dias)):
                    clase_data = {
                        'dia': dias[i], 'espacio': espacios[i],
                        'hora_inicio': horas_inicio[i], 'hora_fin': horas_fin[i],
                        'costo': costos[i], 'cupo_maximo': cupo_global
                    }
                    clase_forms.append(ClaseForm(clase_data, actividad=actividad))
                return render(request, 'create_turno.html', {
                    'turno_form': turno_form, 'clase_forms': clase_forms, 'cupo_maximo': cupo_global
                })
            clases_validas = []
            hay_errores = False
            
            for i in range(len(dias)):
                clase_data = {
                    'dia': dias[i], 'espacio': espacios[i],
                    'hora_inicio': horas_inicio[i], 'hora_fin': horas_fin[i],
                    'costo': costos[i], 'cupo_maximo': cupo_global
                }
                
                clase_form = ClaseForm(clase_data, actividad=actividad)
                clase_forms.append(clase_form)
                
                if clase_form.is_valid():
                    clases_validas.append(clase_form.save(commit=False))
                else:
                    hay_errores = True
                    for error in clase_form.non_field_errors():
                        messages.error(request, f"Error en la Clase {i+1}: {error}")
        
            # Validar superposición entre las clases nuevas del mismo turno
            for i, clase1 in enumerate(clases_validas):
                for j, clase2 in enumerate(clases_validas):
                    if i >= j:
                        continue

                    if clase1.dia == clase2.dia:
                        if (
                            clase1.hora_inicio < clase2.hora_fin
                            and clase1.hora_fin > clase2.hora_inicio
                        ):
                            hay_errores = True
                            messages.error(
                                request,
                                f"Las clases {i+1} y {j+1} tienen horarios superpuestos."
                            )

                        messages.error(request, f"Error en horario {i+1}: {error}")
            
            if not hay_errores and clases_validas:
                turno = turno_form.save()
                for clase in clases_validas:
                    clase.turno = turno
                    clase.save()
                    
                turno.generar_clases_programadas()
                messages.success(request, 'La operación fue realizada con éxito.')
                return redirect('turno_list')
        else:
            actividad = None
            dias = request.POST.getlist('dia')
            espacios = request.POST.getlist('espacio')
            horas_inicio = request.POST.getlist('hora_inicio')
            horas_fin = request.POST.getlist('hora_fin')
            costos = request.POST.getlist('costo')

            for i in range(len(dias)):
                clase_data = {
                    'dia': dias[i], 'espacio': espacios[i],
                    'hora_inicio': horas_inicio[i], 'hora_fin': horas_fin[i],
                    'costo': costos[i], 'cupo_maximo': cupo_global
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
            .annotate(
                inscripciones_activas=Count(
                    "inscripcion",
                    filter=Q(inscripcion__estado='ACTIVA')
                )
            )
            .order_by("actividad__nombre", "nombre")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hoy = timezone.localdate()
        calendario = Calendar(firstweekday=0)
        semanas = calendario.monthdatescalendar(hoy.year, hoy.month)

        context["actividades_asignadas_ids"] = set(
            EmpleadoActividad.objects.filter(empleado=self.request.user).values_list("actividad_id", flat=True)
        )

        meses_es = [
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre",
        ]
        context["calendario_mes"] = meses_es[hoy.month - 1]
        context["calendario_anio"] = hoy.year

        for turno in context["turnos"]:
            clases_programadas = turno.get_clases_programadas().filter(
                fecha__year=hoy.year,
                fecha__month=hoy.month,
            ).select_related("clase").order_by("fecha", "clase__hora_inicio")

            programadas_por_fecha = {}
            for clase_programada in clases_programadas:
                programadas_por_fecha.setdefault(clase_programada.fecha, []).append(clase_programada)

            calendario_turno = []
            for semana in semanas:
                semana_calendario = []
                for fecha in semana:
                    semana_calendario.append({
                        "fecha": fecha,
                        "fuera_mes": fecha.month != hoy.month,
                        "clases_programadas": programadas_por_fecha.get(fecha, []),
                    })
                calendario_turno.append(semana_calendario)

            turno.calendario_mensual = calendario_turno
            turno.tiene_programaciones_mes = bool(programadas_por_fecha)

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

        if self.object.esta_en_curso_ahora():
            messages.error(request, "No se pueden modificar los turnos que están en curso.")
            return self.form_invalid(turno_form)
        
        if not turno_form.is_valid():
            return self.form_invalid(turno_form)

        clase_ids = request.POST.getlist('clase_id')
        dias = request.POST.getlist('dia')
        espacios = request.POST.getlist('espacio')
        horas_inicio = request.POST.getlist('hora_inicio')
        horas_fin = request.POST.getlist('hora_fin')
        costos = request.POST.getlist('costo')
        cupo_global = request.POST.get('cupo_maximo')
        
        if not dias or len(dias) == 0:
            messages.error(request, "El turno debe tener al menos una clase asociada.")
            return self.form_invalid(turno_form)

        # Cupo máximo (Regla 4)
        cupo_int = int(cupo_global) if cupo_global and cupo_global.isdigit() else 0
        if cupo_int <= 0:
            messages.error(request, "El cupo máximo debe ser mayor a 0.")
            return self.form_invalid(turno_form)

        actividad = turno_form.cleaned_data['actividad']
        ids_recibidos = [int(i) for i in clase_ids if i.isdigit()]

        hubo_modificacion = turno_form.has_changed()
        hay_errores = False
        clases_a_guardar = []
        clases_a_eliminar = []

        for clase in self.object.clase_set.filter(activo=True):
            if clase.id not in ids_recibidos:
                hubo_modificacion = True
                clases_a_eliminar.append(clase)

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
                hubo_modificacion = True
                clase_form = ClaseForm(clase_data, actividad=actividad) 
            
            if clase_form.is_valid():
                if clase_form.has_changed():
                    hubo_modificacion = True
                clases_a_guardar.append(clase_form)
            else:
                hay_errores = True
                for error in clase_form.non_field_errors():
                    messages.error(request, error)

        if not hay_errores:
            if hubo_modificacion:
                from reservas.models import Inscripcion, EstadoInscripcion

                inscripciones_activas = Inscripcion.objects.filter(turno=self.object, estado=EstadoInscripcion.ACTIVA)
                for inscripcion in inscripciones_activas:
                    inscripcion.cancelar(por_modificacion_empleado=True)
                if inscripciones_activas.exists():
                    messages.success(request, 'Turno actualizado. Las inscripciones previas fueron canceladas y se generaron los vales correspondientes.')
                else:
                    messages.success(request, 'Turno actualizado.')

            turno = turno_form.save()
            
            for clase in clases_a_eliminar:
                clase.activo = False
                clase.save()
                
            for form in clases_a_guardar:
                if form.instance.pk and form.has_changed():
                    # Clase existente modificada: desactiva la vieja y crea una nueva.
                    # Así las Reserva/ClaseProgramada históricas siguen apuntando
                    # a la clase original con los datos que el socio reservó.
                    form.instance.activo = False
                    form.instance.save()
                    Clase.objects.create(
                        turno=turno,
                        dia=form.cleaned_data['dia'],
                        espacio=form.cleaned_data['espacio'],
                        hora_inicio=form.cleaned_data['hora_inicio'],
                        hora_fin=form.cleaned_data['hora_fin'],
                        costo=form.cleaned_data['costo'],
                        cupo_maximo=form.cleaned_data['cupo_maximo'],
                        activo=True
                    )
                elif not form.instance.pk:
                    # Clase nueva: creacion normal
                    nueva_clase = form.save(commit=False)
                    nueva_clase.turno = turno
                    nueva_clase.save()
                # else: clase existente sin cambios → no hace nada

            if hubo_modificacion:
                self.object.generar_clases_programadas()
                
            return redirect(self.success_url)
        
        return self.form_invalid(turno_form)

# Soft Delete, turno y clases asociadas se desactivan (pero siguen estando en la DB)
class TurnoDeleteView(TurnoActividadRequiredMixin, DeleteView):
    model = Turno
    template_name = 'turnos/turno_confirm_delete.html'
    success_url = reverse_lazy('turno_list')

    def get_queryset(self):
        return Turno.objects.filter(activo=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from reservas.models import Inscripcion, EstadoInscripcion, Reserva, EstadoReserva
        context['en_curso'] = self.object.esta_en_curso_ahora()
        context['inscripciones_activas'] = Inscripcion.objects.filter(
            turno=self.object, estado=EstadoInscripcion.ACTIVA
        ).count()
        # Reservas de socios que NO están inscriptos (clases individuales)
        users_inscriptos = Inscripcion.objects.filter(
            turno=self.object, estado=EstadoInscripcion.ACTIVA
        ).values_list('user_id', flat=True)
        context['reservas_individuales'] = Reserva.objects.filter(
            clase_programada__clase__turno=self.object,
            estado=EstadoReserva.ACTIVA
        ).exclude(user_id__in=users_inscriptos).count()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Regla 4: No se puede eliminar un turno en transcurso
        if self.object.esta_en_curso_ahora():
            messages.error(
                request,
                f'No se puede eliminar el turno "{self.object.nombre}" porque está en transcurso.'
            )
            return redirect(self.success_url)

        # Cancelar inscripciones activas (genera vales para reservas pagas)
        from reservas.models import Inscripcion, EstadoInscripcion, Reserva, EstadoReserva
        inscripciones = Inscripcion.objects.filter(turno=self.object, estado=EstadoInscripcion.ACTIVA)
        cantidad_inscripciones = inscripciones.count()
        vales_totales = 0
        for inscripcion in inscripciones:
            vales_totales += inscripcion.cancelar(por_modificacion_empleado=True)

        # Marcar seña devuelta para socios con clases individuales pagas
        reservas_individuales_pagas = Reserva.objects.filter(
            clase_programada__clase__turno=self.object,
            estado=EstadoReserva.ACTIVA,
            pago_confirmado=True
        )
        cant_devoluciones_individuales = reservas_individuales_pagas.count()
        reservas_individuales_pagas.update(sena_devuelta=True)

        # Desactivar turno y clases (soft delete)
        self.object.desactivar()

        # Construir mensaje
        partes = []
        if cantidad_inscripciones > 0:
            partes.append(f'{cantidad_inscripciones} inscripci{"ón" if cantidad_inscripciones == 1 else "ones"} cancelada{"s" if cantidad_inscripciones > 1 else ""}')
        if vales_totales > 0:
            partes.append(f'{vales_totales} vale{"s" if vales_totales > 1 else ""} de reembolso generado{"s" if vales_totales > 1 else ""}')
        if cant_devoluciones_individuales > 0:
            partes.append(f'devolución de seña a {cant_devoluciones_individuales} socio{"s" if cant_devoluciones_individuales > 1 else ""} con clase{"s" if cant_devoluciones_individuales > 1 else ""} individual{"es" if cant_devoluciones_individuales > 1 else ""}')

        if partes:
            messages.success(request, f'Turno "{self.object.nombre}" eliminado. {", ".join(partes)}.')
        else:
            messages.success(request, f'Turno "{self.object.nombre}" eliminado con éxito.')

        return redirect(self.success_url)

