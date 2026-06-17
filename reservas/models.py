from django.db import models
from datetime import datetime, timedelta
from django.utils import timezone
from turnos.models import ClaseProgramada

class EstadoReserva(models.TextChoices):
    ACTIVA = 'ACTIVA', 'Activa'
    CANCELADA = 'CANCELADA', 'Cancelada'
    PRESENTE = 'PRESENTE', 'Presente'
    AUSENTE = 'AUSENTE', 'Ausente'

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

    class Meta:
        ordering = ['estado', '-fecha_reserva']
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'

    @property
    def corresponde_devolucion(self):
        if self.estado == EstadoReserva.CANCELADA and self.pago_confirmado and not self.clase_programada.ya_empezo:
            if self.fecha_cancelacion:
                fecha_hora_clase = datetime.combine(
                    self.clase_programada.fecha, 
                    self.clase_programada.clase.hora_inicio
                )
                fecha_hora_clase = timezone.make_aware(fecha_hora_clase, timezone.get_current_timezone())
                tiempo_anticipacion = fecha_hora_clase - self.fecha_cancelacion
                return tiempo_anticipacion >= timedelta(hours=24)
        return False
    
    def desactivar(self, informar=False, motivo='', por_empleado=False):
        if self.estado != EstadoReserva.CANCELADA:
            self.estado = EstadoReserva.CANCELADA
            self.fecha_cancelacion = timezone.now()
            self.save()
        self.devolver_pago(por_empleado)

    def devolver_pago(self, por_empleado=False):
        if self.clase_programada.ya_empezo:
            return

        if (self.corresponde_devolucion or por_empleado) and not self.sena_devuelta:
            if hasattr(self.user, 'credito'):
                self.user.credito.agregar_credito(self.clase_programada.clase.costo)
                self.sena_devuelta = True
                self.save()
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
        clases_programadas = self.turno.get_clases_programadas().filter(
            fecha__gte = timezone.localdate()
        )

        # si el usuario no tiene ya una reserva activa, le creo una
        for clase_programada in clases_programadas:
            if (not Reserva.objects.filter(user=self.user, clase_programada=clase_programada, estado=EstadoReserva.ACTIVA).exists()):
                Reserva.objects.create(user=self.user, clase_programada=clase_programada)
    
    def cancelar(self, por_modificacion_empleado=False):
        self.estado = EstadoInscripcion.DE_BAJA
        self.fecha_baja = timezone.now()
        self.save()
        
        clases_programadas = self.turno.get_clases_programadas().filter(
            fecha__gte=timezone.localdate()
        )
        
        reservas_usuario = Reserva.objects.filter(
            user=self.user,
            clase_programada__in=clases_programadas,
            estado=EstadoReserva.ACTIVA
        )
        
        for reserva in reservas_usuario:
            reserva.desactivar(informar=por_modificacion_empleado, motivo='El turno fue modificado' if por_modificacion_empleado else '', por_empleado=por_modificacion_empleado)