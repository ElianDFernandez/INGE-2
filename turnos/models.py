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
        return self.clase_set.filter(activo=True).exists()
    
    def get_clases_activas(self):
        return self.clase_set.filter(activo=True)
    
    def desactivar(self):
        self.activo = False
        self.save()

        for clase in self.clase_set.filter(activo=True):
            clase.desactivar()

    def generar_clases_programadas(self):
        for clase in self.get_clases_activas():
            clase.generar_clases_programadas()

    def admite_inscripcion(self, user):
        from reservas.models import Reserva, EstadoReserva

        for clase in self.get_clases_activas():
            for cp in clase.claseprogramada_set.filter(fecha__gte=timezone.localdate()):
                # si el usuario ya tiene reserva no me restringe la inscripcion
                if Reserva.objects.filter(user=user, clase_programada=cp, estado=EstadoReserva.ACTIVA).exists():
                    continue

                if cp.cupo_actual() >= clase.cupo_maximo:
                    return False
        return True

    def get_clases_programadas(self):
        return ClaseProgramada.objects.filter(
            clase__turno=self,
            clase__activo=True
        )

class Clase(models.Model):
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE)
    dia = models.CharField(max_length=10, choices=DiaSemana.choices)
    espacio = models.CharField(max_length=20, choices=Espacio.choices)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    costo = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    cupo_maximo = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    activo = models.BooleanField(default=True)

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

        fecha = timezone.localdate()
        cur_mes = fecha.month
        prox_mes = cur_mes + 1 if cur_mes < 12 else 1

        while fecha.weekday() != dias[self.dia]:
            fecha += timedelta(days=1)

        # cambiar, nomas para testing
        while (fecha.month==cur_mes) or (fecha.month==prox_mes):
            ClaseProgramada.objects.get_or_create(clase=self, fecha=fecha)
            fecha += timedelta(days=7)

    def tiene_reservas(self):
        from reservas.models import Reserva, EstadoReserva

        return Reserva.objects.filter(
            clase_programada__clase=self
        ).exclude(estado=EstadoReserva.CANCELADA).exists()

    def tiene_reservas_proximas(self):
        from datetime import datetime
        from reservas.models import Reserva, EstadoReserva

        ahora = timezone.now()
        fecha_limite = ahora + timedelta(hours=24)

        reservas = Reserva.objects.filter(clase_programada__clase=self,  estado=EstadoReserva.ACTIVA)

        # combinamos fecha y hora de cada reserva
        for reserva in reservas:
            fecha_hora_clase = timezone.make_aware(
                datetime.combine(
                    reserva.clase_programada.fecha,
                    self.hora_inicio
                )
            )
            
            # toda clase cuya fecha cae entre hoy y 24 horas despues no puede ser editada
            if ahora <= fecha_hora_clase <= fecha_limite:
                return True
        return False

    def desactivar(self):
        from reservas.models import Reserva, EstadoReserva

        self.activo = False
        self.save()

        # desactivo toda reserva activa de esta clase
        Reserva.objects.filter(
            clase_programada__clase=self, estado=EstadoReserva.ACTIVA).update(
            estado=EstadoReserva.CANCELADA,
            fecha_cancelacion=timezone.now()
        )

class ClaseProgramada(models.Model):
    clase = models.ForeignKey(Clase, on_delete=models.CASCADE)
    fecha = models.DateField()

    def cupo_actual(self):
        # estado está hardcodeado y no lo saco del choices de reservas pq los import quedan circular
        return self.reserva_set.filter(estado='ACTIVA').count()

    class Meta:
        ordering = ['fecha', 'clase__hora_inicio']
        unique_together = ('clase', 'fecha')