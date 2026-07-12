from datetime import datetime, timedelta

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from turnos.models import ClaseProgramada

# Create your models here.
class EstadoListaEspera(models.TextChoices):
    PENDIENTE = 'pendiente', 'Pendiente'
    CONFIRMADO = 'confirmado', 'Confirmado'
    CANCELADO = 'cancelado', 'Cancelado'
    NOTIFICADO = 'notificado', 'Notificado'
    EXPIRADO = 'expirado', 'Expirado'


class ListaEspera(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lista_espera')
    clase_programada = models.ForeignKey(ClaseProgramada, on_delete=models.CASCADE, related_name='lista_espera')
    fecha_anotacion = models.DateTimeField(auto_now_add=True)
    fecha_notificacion = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=EstadoListaEspera.choices, default=EstadoListaEspera.PENDIENTE)

    class Meta:
        ordering = ['fecha_anotacion']
        unique_together = ['user', 'clase_programada']

    def __str__(self):
        return f"{self.user} - {self.clase_programada} ({self.estado})"

    def _fecha_notificacion_aware(self):
        if self.fecha_notificacion is None:
            return None

        fecha = self.fecha_notificacion
        if isinstance(fecha, datetime) and timezone.is_naive(fecha):
            return timezone.make_aware(fecha)

        return fecha

    def puede_confirmar(self):
        if self.estado != EstadoListaEspera.NOTIFICADO:
            return False

        fecha_notificacion = self._fecha_notificacion_aware()
        if fecha_notificacion is None:
            return False

        return timezone.now() <= fecha_notificacion + timedelta(hours=2)

    @property
    def tiempo_restante_para_confirmar(self):
        fecha_notificacion = self._fecha_notificacion_aware()
        if fecha_notificacion is None:
            return None
        deadline = fecha_notificacion + timedelta(hours=2)
        return max(deadline - timezone.now(), timedelta(seconds=0))
    
    def get_posicion(self):
        return ListaEspera.objects.filter(
            clase_programada=self.clase_programada,
            estado=EstadoListaEspera.PENDIENTE,
            fecha_anotacion__lt=self.fecha_anotacion
        ).count() + 1