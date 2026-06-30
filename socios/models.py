from django.contrib.auth.models import User, UserManager
from django.utils import timezone
from django.db import models

class SocioManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_staff=False, is_superuser=False)
    
class Socio(User):
    objects = SocioManager()

    class Meta:
        proxy = True
        verbose_name = 'Socio'
        verbose_name_plural = 'Socios'

    def get_reservas(self):
        return self.reservas.all().order_by('-fecha_reserva')
    
    def get_reservas_en_periodo(self, dias):
        hoy = timezone.localdate()
        fin_periodo = hoy + timezone.timedelta(days=dias)
        
        return self.reservas.filter(clase_programada__fecha__range=(hoy, fin_periodo)).order_by('clase_programada__fecha', 'clase_programada__clase__hora_inicio')

    def get_contexto_home(self):
        hoy = timezone.localdate()
        fin_rango_calendario = hoy + timezone.timedelta(days=6)
        reservas_semana = self.get_reservas_en_periodo(7).filter(estado='ACTIVA')
        
        reservas_por_fecha = {}
        for reserva in reservas_semana:
            fecha = reserva.clase_programada.fecha
            reservas_por_fecha.setdefault(fecha, []).append({
                'actividad': reserva.clase_programada.clase.turno.actividad.nombre,
                'hora_inicio': reserva.clase_programada.clase.hora_inicio,
                'hora_fin': reserva.clase_programada.clase.hora_fin,
                'espacio': reserva.clase_programada.clase.get_espacio_display(),
            })

        dias_semana = []
        for offset in range(7):
            fecha = hoy + timezone.timedelta(days=offset)
            dias_semana.append({
                'fecha': fecha,
                'reservas': reservas_por_fecha.get(fecha, []),
                'es_hoy': fecha == hoy,
            })

        clases_totales_mes = self.reservas.filter(
            clase_programada__fecha__year=hoy.year,
            clase_programada__fecha__month=hoy.month,
            estado='ACTIVA'
        )
        
        total_clases = clases_totales_mes.count()
        asistencias = clases_totales_mes.filter(asistio=True).count()
        
        porcentaje_asistencia = 0
        if total_clases > 0:
            porcentaje_asistencia = int((asistencias / total_clases) * 100)

        return {
            'dias_semana': dias_semana,
            'rango_semana': f"{hoy.strftime('%d/%m')} al {fin_rango_calendario.strftime('%d/%m')}",
            'asistencias_mes': asistencias,
            'total_clases_mes': total_clases,
            'porcentaje_asistencia': porcentaje_asistencia,
        }

    def get_vales_disponibles(self):
        """Retorna los vales disponibles (no usados y no vencidos)."""
        hoy = timezone.localdate()
        return self.vales.filter(usado=False, fecha_vencimiento__gte=hoy)

    def get_vales_disponibles_por_actividad(self, actividad):
        """Retorna vales disponibles para una actividad específica."""
        return self.get_vales_disponibles().filter(actividad=actividad)

    def tiene_vale_para_actividad(self, actividad):
        """Verifica si el socio tiene un vale disponible para una actividad."""
        return self.get_vales_disponibles_por_actividad(actividad).exists()
    
    def get_cancelaciones(self):
        """Retorna las cancelaciones de inscripciones del mes anterior."""
        from reservas.models import Inscripcion, EstadoInscripcion
        hoy = timezone.localdate()
        primer_dia_mes_anterior = (hoy.replace(day=1) - timezone.timedelta(days=1)).replace(day=1)
        ultimo_dia_mes_anterior = hoy.replace(day=1) - timezone.timedelta(days=1)

        return Inscripcion.objects.filter(
            user=self,
            estado=EstadoInscripcion.DE_BAJA,
            fecha_baja__date__range=(primer_dia_mes_anterior, ultimo_dia_mes_anterior)
        ).order_by('-fecha_baja')

class Vale(models.Model):
    socio = models.ForeignKey(Socio, on_delete=models.CASCADE, related_name='vales')
    actividad = models.ForeignKey('actividades.Actividad', on_delete=models.CASCADE, related_name='vales')
    fecha_emision = models.DateField(auto_now_add=True)
    fecha_vencimiento = models.DateField()
    usado = models.BooleanField(default=False)
    fecha_uso = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Vale'
        verbose_name_plural = 'Vales'
        ordering = ['-fecha_emision']

    def __str__(self):
        estado = "Usado" if self.usado else "Disponible"
        return f"Vale de {self.socio.username} para {self.actividad.nombre} ({estado})"

    def usar(self):
        """Marca el vale como usado."""
        if self.usado:
            raise ValueError("Este vale ya fue utilizado")
        self.usado = True
        self.fecha_uso = timezone.now()
        self.save()

    def esta_vencido(self):
        """Verifica si el vale ha vencido."""
        return timezone.localdate() > self.fecha_vencimiento

    def get_estado_display(self):
        """Retorna el estado legible del vale."""
        if self.usado:
            return "Usado"
        elif self.esta_vencido():
            return "Vencido"
        return "Disponible"

    def get_dias_restantes(self):
        """Retorna los días restantes antes del vencimiento."""
        if self.usado:
            return 0
        hoy = timezone.localdate()
        dias = (self.fecha_vencimiento - hoy).days
        return max(0, dias)