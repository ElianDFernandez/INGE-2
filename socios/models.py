import calendar

from django.contrib.auth.models import User, UserManager
from django.utils import timezone
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

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
    
@receiver(post_save, sender=User)
def crear_credito_para_socio(sender, instance, created, **kwargs):
    if created and not instance.is_superuser and not instance.is_staff:
        Credito.objects.create(socio=instance)
    
class Credito(models.Model):
    socio = models.OneToOneField(Socio, on_delete=models.CASCADE, related_name='credito')
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Crédito de {self.socio.username}: ${self.saldo}"
    
    def agregar_credito(self, monto):
        self.saldo += monto
        self.save()

    def descontar_credito(self, monto):
        if monto > self.saldo:
            raise ValueError("Saldo insuficiente")
        self.saldo -= monto
        self.save()

    def consultar_credito(self):
        return self.saldo
    
    def reiniciar_credito(self):
        self.saldo = 0
        self.save()

    def get_vencimiento(self):
        hoy = timezone.localdate()
        _, ultimo_dia = calendar.monthrange(hoy.year, hoy.month)
        fecha = hoy.replace(day=ultimo_dia)
        return fecha.strftime("%d/%m/%Y")