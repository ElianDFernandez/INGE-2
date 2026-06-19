from django.db import models
from datetime import datetime, timedelta
from django.utils import timezone
from turnos.models import ClaseProgramada
import uuid
class EstadoReserva(models.TextChoices):
    ACTIVA = 'ACTIVA', 'Activa'
    CANCELADA = 'CANCELADA', 'Cancelada'
class MetodoAsistencia(models.TextChoices):
    MANUAL = 'MANUAL', 'Manual'
    QR = 'QR', 'Código QR'
class MetodoPago(models.TextChoices):
    MANUAL = 'MANUAL', 'Manual (Recepción)'
    VIRTUAL = 'VIRTUAL', 'Virtual (MercadoPago/Transferencia)'

class Reserva(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='reservas')
    clase_programada = models.ForeignKey(ClaseProgramada, on_delete=models.CASCADE)
    fecha_reserva = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=EstadoReserva.choices, default=EstadoReserva.ACTIVA)
    fecha_cancelacion = models.DateTimeField(null=True, blank=True)
    metodo_asistencia = models.CharField(max_length=20, choices=MetodoAsistencia.choices, null=True, blank=True, default=None)
    asistio = models.BooleanField(default=False)
    pago_confirmado = models.BooleanField(default=False)
    metodo_pago = models.CharField(max_length=20, choices=MetodoPago.choices, null=True, blank=True)
    sena_devuelta = models.BooleanField(default=False)
    qr_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def desactivar(self, informar = False, motivo = ''):
        if self.estado != EstadoReserva.CANCELADA:
            self.estado = EstadoReserva.CANCELADA
            self.fecha_cancelacion = timezone.now()
            self.save()

    @property
    def corresponde_devolucion(self):
        if self.estado == EstadoReserva.CANCELADA and self.pago_confirmado:
            if self.fecha_cancelacion:
                fecha_hora_clase = datetime.combine(
                    self.clase_programada.fecha, 
                    self.clase_programada.clase.hora_inicio
                )
                fecha_hora_clase = timezone.make_aware(fecha_hora_clase, timezone.get_current_timezone())
                tiempo_anticipacion = fecha_hora_clase - self.fecha_cancelacion
                return tiempo_anticipacion >= timedelta(hours=24)
        return False

    class Meta:
        ordering = ['estado', '-fecha_reserva']
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'


class EstadoInscripcion(models.TextChoices):
    ACTIVA = 'ACTIVA', 'Activa'
    DE_BAJA = 'DE_BAJA', 'De Baja'

class Inscripcion(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    turno = models.ForeignKey('turnos.Turno', on_delete=models.CASCADE)

    fecha_alta = models.DateTimeField(auto_now_add=True)
    fecha_baja = models.DateTimeField(null=True, blank=True)

    estado = models.CharField(max_length=20, choices=EstadoInscripcion.choices, default=EstadoInscripcion.ACTIVA)

    def reservar_clases_programadas(self):
        clases_prog = self.turno.get_clases_programadas().filter(
            fecha__gte = timezone.localdate()
        )

        # si el usuario no tiene ya una reserva activa, le creo una
        for clase in clases_prog:
            if (not Reserva.objects.filter(user=self.user, clase_programada=clase, estado=EstadoReserva.ACTIVA).exists()):
                Reserva.objects.create(user=self.user, clase_programada=clase)
    

    def cancelar_clases_programadas(self):
        clases_prog = self.turno.get_clases_programadas().filter(
            fecha__gte = timezone.localdate()
        )

        for clase in clases_prog:
            Reserva.objects.filter(user=self.user, 
                                   clase_programada=clase, 
                                   estado=EstadoReserva.ACTIVA
                                   ).update(estado=EstadoReserva.CANCELADA)