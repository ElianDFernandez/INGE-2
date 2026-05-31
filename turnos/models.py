from datetime import timedelta
from django.db import models
from django.utils import timezone
from actividades.models import Actividad
from django.core.validators import MinValueValidator
from django.db.models import F
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

    @property
    def cupos_ocupados(self):
        return self.max_reservas_actuales()

    @property
    def cupo_maximo(self):
        primera_clase = self.clase_set.filter(activo=True).first()
        return primera_clase.cupo_maximo if primera_clase else 0
    
    @property
    def hay_cupo(self):
        return self.cupos_ocupados < self.cupo_maximo

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
        for clase in self.clases_activas():
            clase.generar_clases_programadas()

    def esta_inscripto(self, user):
        return self.inscripcion_set.filter(user=user, estado='ACTIVA').exists()
    
    def tiene_cupo_disponible(self):
        todas_las_clases = self.get_clases_programadas()
        if not todas_las_clases.exists():
            return False 
        for clase_prog in todas_las_clases:
            if clase_prog.cupo_actual() >= clase_prog.clase.cupo_maximo:
                return False
        return True

    def get_clases_programadas(self):
        return ClaseProgramada.objects.filter(
            clase__turno=self,
            clase__activo=True
        )
    
    def max_reservas_actuales(self):
        from django.db.models import Count, Q, Max
        from django.utils import timezone
        from reservas.models import EstadoReserva
        clases_futuras = self.get_clases_programadas().filter(fecha__gte=timezone.localdate())
        resultado = clases_futuras.annotate(
            num_reservas=Count('reserva', filter=Q(reserva__estado=EstadoReserva.ACTIVA))
        ).aggregate(max_r=Max('num_reservas'))

        return resultado['max_r'] or 0

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
        from reservas.models import Reserva, EstadoReserva
        dias = {
            'LUNES': 0, 'MARTES': 1, 'MIERCOLES': 2, 'JUEVES': 3,
            'VIERNES': 4, 'SABADO': 5, 'DOMINGO': 6,
        }
        fecha = timezone.localdate()
        cur_mes = fecha.month
        prox_mes = cur_mes + 1 if cur_mes < 12 else 1
        while fecha.weekday() != dias[self.dia]:
            fecha += timedelta(days=1)
        inscripciones_activas = self.turno.inscripcion_set.filter(estado='ACTIVA').select_related('user')
        reservas_a_crear = []
        while (fecha.month==cur_mes) or (fecha.month==prox_mes):
            cp, created = ClaseProgramada.objects.get_or_create(clase=self, fecha=fecha)
            if created:
                for inscripcion in inscripciones_activas:
                    reservas_a_crear.append(
                        Reserva(
                            user=inscripcion.user,
                            clase_programada=cp,
                            estado=EstadoReserva.ACTIVA
                        )
                    )
            fecha += timedelta(days=7)
        if reservas_a_crear:
            Reserva.objects.bulk_create(reservas_a_crear)

    def tiene_reservas(self):
        from reservas.models import Reserva, EstadoReserva
        return Reserva.objects.filter(
            clase_programada__clase=self, estado=EstadoReserva.ACTIVA).exists()

    def tiene_reservas_proximas(self):
        from datetime import datetime, timedelta
        from django.utils import timezone
        from reservas.models import EstadoReserva
        ahora = timezone.now()
        fecha_limite = ahora + timedelta(hours=24)
        clases_cercanas = self.claseprogramada_set.filter(
            fecha__gte=ahora.date(),
            fecha__lte=fecha_limite.date()
        )
        for cp in clases_cercanas:
            fecha_hora_clase = timezone.make_aware(
                datetime.combine(cp.fecha, self.hora_inicio)
            )
            if ahora <= fecha_hora_clase <= fecha_limite:
                if cp.reserva_set.filter(estado=EstadoReserva.ACTIVA).exists():
                    return True

        return False

    def desactivar(self, informar = False, motivo = ''):
        from reservas.models import Reserva, EstadoReserva

        self.activo = False
        self.save()

        reservas_activas = Reserva.objects.filter(clase_programada__clase=self, estado=EstadoReserva.ACTIVA)
        for reserva in reservas_activas:
            reserva.desactivar(informar, motivo)

    def puede_modificar(self):
        return not self.tiene_reservas_proximas()
    
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
        
        nueva_clase.generar_clases_programadas()
        
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

    def dia(self):
        dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        return dias[self.fecha.weekday()]

    def cupo_actual(self):
        # estado está hardcodeado y no lo saco del choices de reservas pq los import quedan circular
        return self.reserva_set.filter(estado='ACTIVA').count()

    class Meta:
        ordering = ['fecha', 'clase__hora_inicio']
        unique_together = ('clase', 'fecha')