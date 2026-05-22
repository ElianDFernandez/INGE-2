from django.contrib.auth.models import User, UserManager
from django.utils import timezone

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
        fin_semana = hoy + timezone.timedelta(days=6)
        reservas_semana = self.get_reservas_en_periodo(7)

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

        return {
            'dias_semana': dias_semana,
            'rango_semana': f"{hoy.strftime('%d/%m')} al {fin_semana.strftime('%d/%m')}",
        }