import calendar
from decimal import Decimal
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

    @property
    def corresponde_devolucion(self):
        if self.estado == EstadoReserva.CANCELADA and self.mp_payment_id and not self.clase_programada.ya_empezo:
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

    def devolver_pago(self):
        """
        Marca la reserva como reembolsada (simulado).
        """
        if self.sena_devuelta:
            return  # ya fue devuelto

        if not self.corresponde_devolucion:
            return  # no corresponde reembolso

        self.sena_devuelta = True
        self.save(update_fields=['sena_devuelta'])
                
class EstadoInscripcion(models.TextChoices):
    INICIADA = 'INICIADA', 'Iniciada (En proceso de pago)'
    ACTIVA = 'ACTIVA', 'Activa'
    DE_BAJA = 'DE_BAJA', 'De Baja'

class Inscripcion(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    turno = models.ForeignKey('turnos.Turno', on_delete=models.CASCADE)

    fecha_alta = models.DateTimeField(auto_now_add=True)
    fecha_baja = models.DateTimeField(null=True, blank=True)

    estado = models.CharField(max_length=20, choices=EstadoInscripcion.choices, default=EstadoInscripcion.ACTIVA)

    # MercadoPago
    mp_preference_id = models.CharField(max_length=255, null=True, blank=True)
    mp_payment_id = models.CharField(max_length=255, null=True, blank=True)

    def reservar_clases_programadas(self):
        clases_programadas = self.turno.get_clases_programadas().filter(
            fecha__gte=timezone.localdate()
        )

        for clase_programada in clases_programadas:
            # Buscar reserva existente (no cancelada)
            reserva_existente = Reserva.objects.filter(
                user=self.user,
                clase_programada=clase_programada
            ).exclude(estado=EstadoReserva.CANCELADA).first()

            if reserva_existente:
                # Ya tiene reserva PENDIENTE_PAGO o ACTIVA → upgradeear a ACTIVA
                if reserva_existente.estado != EstadoReserva.ACTIVA:
                    reserva_existente.estado = EstadoReserva.ACTIVA
                    reserva_existente.pago_confirmado = True
                    reserva_existente.save()
            else:
                # Sin reserva → crear nueva ACTIVA
                Reserva.objects.create(
                    user=self.user,
                    clase_programada=clase_programada,
                    estado=EstadoReserva.ACTIVA,
                    pago_confirmado=True
                )
    
    def generar_vales_devolucion(self, por_modificacion_empleado=False):
        """
        Genera vales para las reservas pagas que se cancelan con al menos 48hs de anticipación.
        Si la cancelación es por modificación del empleado, se considera que cumple el plazo.
        """
        from socios.models import Vale

        hoy = timezone.localdate()
        _, ultimo_dia = calendar.monthrange(hoy.year, hoy.month)
        fecha_vencimiento = hoy.replace(day=ultimo_dia)

        clases_programadas = self.turno.get_clases_programadas().filter(
            fecha__gte=hoy
        )

        reservas_pagas = Reserva.objects.filter(
            user=self.user,
            clase_programada__in=clases_programadas,
            estado=EstadoReserva.ACTIVA,
        )

        vales_creados = 0
        ahora = timezone.now()

        for reserva in reservas_pagas:
            if por_modificacion_empleado:
                generar = True
            else:
                fecha_hora_clase = datetime.combine(
                    reserva.clase_programada.fecha,
                    reserva.clase_programada.clase.hora_inicio
                )
                fecha_hora_clase = timezone.make_aware(fecha_hora_clase, timezone.get_current_timezone())
                anticipacion = fecha_hora_clase - ahora
                generar = anticipacion >= timedelta(hours=48)

            if generar:
                Vale.objects.create(
                    socio_id=self.user_id,
                    actividad=self.turno.actividad,
                    fecha_vencimiento=fecha_vencimiento
                )
                reserva.sena_devuelta = True
                reserva.save(update_fields=['sena_devuelta'])
                vales_creados += 1

        return vales_creados

    def cancelar(self, por_modificacion_empleado=False):
        vales_creados = self.generar_vales_devolucion(por_modificacion_empleado=por_modificacion_empleado)

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

        return vales_creados
    
    def get_costo(self):
        """
        Retorna el costo total que el usuario debe pagar por el turno.
        - Clases sin reserva: costo completo (100%).
        - Clases con reserva ACTIVA: ya pagó el 100%, no se cuenta.
        - Clases con reserva PENDIENTE_PAGO: pagó el 50%, se cuenta el 50% restante.
        """
        clases_programadas = self.turno.get_clases_programadas().filter(
            fecha__gte=timezone.localdate()
        )
        costo_total = Decimal('0')
        for cp in clases_programadas:
            reserva = Reserva.objects.filter(
                user=self.user,
                clase_programada=cp
            ).exclude(estado=EstadoReserva.CANCELADA).first()
            if reserva is None:
                # Sin reserva: se paga el costo completo
                costo_total += cp.clase.costo
            elif reserva.estado == EstadoReserva.PENDIENTE_PAGO:
                # Ya pagó la seña (50%), se cobra el restante
                costo_total += cp.clase.costo * Decimal('0.50')
            # ACTIVA ya está pagada al 100%, no suma
        return costo_total

    def get_costo_final(self):
        """
        Retorna el costo final del turno, aplicando descuentos si aplica.
        - 20% de descuento si socio.get_cancelaciones() < 3.
        """
        from socios.models import Socio
        costo_total = self.get_costo()
        descuento = Decimal('0')
        try:
            socio = Socio.objects.get(pk=self.user_id)
            if socio.get_cancelaciones().count() < 3:
                descuento = costo_total * Decimal('0.20')
        except Exception:
            pass  # Si no tiene socio asociado, no aplica descuento
        costo_final = costo_total - descuento
        return costo_final




    

