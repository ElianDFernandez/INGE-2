from django.db import models
from datetime import datetime, timedelta
from django.utils import timezone
from turnos.models import ClaseProgramada
import uuid
class EstadoReserva(models.TextChoices):
    INICIADA = 'INICIADA', 'Iniciada (En proceso de pago)'
    ACTIVA = 'ACTIVA', 'Activa (Pagado 100%)'
    CANCELADA = 'CANCELADA', 'Cancelada'
    PRESENTE = 'PRESENTE', 'Presente'
    AUSENTE = 'AUSENTE', 'Ausente'
    PENDIENTE_PAGO = 'PENDIENTE_PAGO', 'Pendiente de Pago (Señada)'

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
    estado = models.CharField(max_length=20, choices=EstadoReserva.choices, default=EstadoReserva.INICIADA)
    fecha_cancelacion = models.DateTimeField(null=True, blank=True)
    metodo_asistencia = models.CharField(max_length=20, choices=MetodoAsistencia.choices, null=True, blank=True, default=None)
    asistio = models.BooleanField(default=False)
    pago_confirmado = models.BooleanField(default=False)
    metodo_pago = models.CharField(max_length=20, choices=MetodoPago.choices, null=True, blank=True)
    sena_devuelta = models.BooleanField(default=False)
    qr_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def save(self, *args, **kwargs):
        if self._state.adding:
            while True:
                # antes de guardarlo en la db me fijo si el token colisiona con el de otra reserva para que no rompa por el unique
                token = uuid.uuid4()
                if not Reserva.objects.filter(qr_token=token).exists():
                    self.qr_token = token
                    break

        super().save(*args, **kwargs)

    # Campo para guardar el ID de preferencia de MercadoPago
    mp_preference_id = models.CharField(max_length=255, null=True, blank=True)
    # Campo para guardar el ID del pago real una vez que se concreta
    mp_payment_id = models.CharField(max_length=255, null=True, blank=True)

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

