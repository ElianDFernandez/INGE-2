from django.db import models
from turnos.models import ClaseProgramada

class EstadoReserva(models.TextChoices):
    ACTIVA = 'ACTIVA', 'Activa'
    CANCELADA = 'CANCELADA', 'Cancelada'

class MetodoAsistencia(models.TextChoices):
    MANUAL = 'MANUAL', 'Manual'
    QR = 'QR', 'Código QR'

class Reserva(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    clase_programada = models.ForeignKey(ClaseProgramada, on_delete=models.CASCADE)
    fecha_reserva = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=EstadoReserva.choices, default=EstadoReserva.ACTIVA)
    fecha_cancelacion = models.DateTimeField(null=True, blank=True)
    metodo_asistencia = models.CharField(max_length=20, choices=MetodoAsistencia.choices, null=True, blank=True, default=None)

    class Meta:
        unique_together = ('user', 'clase_programada')
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'