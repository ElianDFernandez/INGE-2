from datetime import timedelta
from django.db import models
from django.utils import timezone
from actividades.models import Actividad
from django.core.validators import MinValueValidator
class DiaSemana(models.TextChoices):
    LUNES = 'LUNES', 'Lunes'
    MARTES = 'MARTES', 'Martes'
    MIERCOLES = 'MIERCOLES', 'Miércoles'
    JUEVES = 'JUEVES', 'Jueves'
    VIERNES = 'VIERNES', 'Viernes'
    SABADO = 'SABADO', 'Sábado'
    DOMINGO = 'DOMINGO', 'Domingo'

class Espacio(models.TextChoices):
    CANCHA_COMBINADA = 'CANCHA_COMBINADA', 'Cancha Combinada'
    CANCHA_PADDLE_1 = 'CANCHA_PADDLE_1', 'Cancha Paddle 1'
    CANCHA_PADDLE_2 = 'CANCHA_PADDLE_2', 'Cancha Paddle 2'
    CANCHA_FUTBOL_1 = 'CANCHA_FUTBOL_1', 'Cancha Fútbol 1'
    CANCHA_FUTBOL_2 = 'CANCHA_FUTBOL_2', 'Cancha Fútbol 2'


class Turno(models.Model):
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)

    def tiene_reservas(self):
        from reservas.models import Reserva, EstadoReserva

        return Reserva.objects.filter(
            clase_programada__clase__turno=self
        ).exclude(estado=EstadoReserva.CANCELADA).exists()

    def tiene_clases(self):
        return self.clase_set.exists()

    def clases_activas(self):
        return self.clase_set.filter(activo=True).order_by('dia', 'hora_inicio')
    
    def desactivar(self):
        self.activo = False
        self.save()

        for clase in self.clase_set.filter(activo=True):
            clase.desactivar()

    def generar_clases_programadas(self):
        dias = {
            'LUNES': 0,
            'MARTES': 1,
            'MIERCOLES': 2,
            'JUEVES': 3,
            'VIERNES': 4,
            'SABADO': 5,
            'DOMINGO': 6,
        }

        for clase in self.clase_set.all():
            fecha = timezone.localdate()
            cur_mes = timezone.localdate().month
            prox_mes = (cur_mes + 1) if cur_mes < 12 else 1

            # me paro en el proximo dia de la semana que le corresponde a esta clase
            while fecha.weekday() != dias[clase.dia]:
                fecha += timedelta(days=1)
            
            while (fecha.month == cur_mes) or (fecha.month == prox_mes):
                ClaseProgramada.objects.get_or_create(clase=clase, fecha=fecha)
                fecha += timedelta(days=7)
class Clase(models.Model):
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE)
    dia = models.CharField(max_length=10, choices=DiaSemana.choices)
    espacio = models.CharField(max_length=20, choices=Espacio.choices)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    costo = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0)])
    cupo_maximo = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    activo = models.BooleanField(default=True)

    def tiene_reservas(self):
        from reservas.models import Reserva, EstadoReserva
        return Reserva.objects.filter(
            clase_programada__clase=self
        ).exclude(estado=EstadoReserva.CANCELADA).exists()
        
    def desactivar(self, informar = False, motivo = ''):
        from reservas.models import Reserva, EstadoReserva

        self.activo = False
        self.save()

        reservas_activas = Reserva.objects.filter(clase_programada__clase=self, estado=EstadoReserva.ACTIVA)
        for reserva in reservas_activas:
            reserva.desactivar()

    def reemplazar_por_modificacion(self, nuevos_datos, informar = False, motivo = ''):
        self.desactivar(informar, motivo)
        nueva_clase = Clase.objects.create(
            turno=self.turno,
            dia=nuevos_datos['dia'],
            espacio=nuevos_datos['espacio'],
            hora_inicio=nuevos_datos['hora_inicio'],
            hora_fin=nuevos_datos['hora_fin'],
            costo=nuevos_datos['costo'],
            cupo_maximo=nuevos_datos['cupo_maximo'],
            activo=True
        )
        # -------------------------------------------------------------
        # TODO: LÓGICA FUTURA
        # Como por ejemplo los socios inscriptos a esta clase, que podrían pasar a la nueva clase o recibir una notificación, etc.
        # -------------------------------------------------------------

        return nueva_clase

    def cancelacion_por_modificacion(self, informar = False, motivo = ''):
        from reservas.models import Reserva, EstadoReserva
        self.desactivar(informar, motivo)
        reservas_activas = Reserva.objects.filter(clase_programada__clase=self, estado=EstadoReserva.ACTIVA)
        for reserva in reservas_activas:
            reserva.desactivar(informar, motivo)


class ClaseProgramada(models.Model):
    clase = models.ForeignKey(Clase, on_delete=models.CASCADE)
    fecha = models.DateField()

    def cupo_actual(self):
        # estado está hardcodeado y no lo saco del choices de reservas pq los import quedan circular
        return self.reserva_set.filter(estado='ACTIVA').count()

    class Meta:
        ordering = ['fecha', 'clase__hora_inicio']
        unique_together = ('clase', 'fecha')