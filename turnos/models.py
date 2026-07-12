from datetime import datetime, timedelta
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
            num_reservas=Count('reserva', filter=Q(reserva__estado__in=[EstadoReserva.ACTIVA, EstadoReserva.PENDIENTE_PAGO]))
        ).aggregate(max_r=Max('num_reservas'))

        return resultado['max_r'] or 0
    
    def esta_en_curso_ahora(self):
        from django.utils import timezone
        hoy = timezone.localdate()
        ahora = timezone.localtime().time()
        return self.clase_set.filter(
            activo=True,
            claseprogramada__fecha=hoy,
            hora_inicio__lte=ahora,
            hora_fin__gte=ahora
        ).exists()

    def se_superponen(self, otroTurno):
        clases_self = list(self.clase_set.filter(activo=True))
        clases_otro = list(otroTurno.clase_set.filter(activo=True))

        for clase1 in clases_self:
            for clase2 in clases_otro:
                if clase1.se_superponen(clase2):
                    return True
        return False

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
        from django.utils import timezone
        from datetime import timedelta
        dias = {
            'LUNES': 0, 'MARTES': 1, 'MIERCOLES': 2, 'JUEVES': 3,
            'VIERNES': 4, 'SABADO': 5, 'DOMINGO': 6,
        }
        ahora = timezone.localtime()
        hoy = ahora.date()

        # Primer día del mes anterior
        if hoy.month == 1:
            fecha = hoy.replace(year=hoy.year - 1, month=12, day=1)
        else:
            fecha = hoy.replace(month=hoy.month - 1, day=1)

        # Primer día del mes siguiente al próximo como límite (genera mes anterior + actual + siguiente)
        if hoy.month >= 11:
            fecha_limite = hoy.replace(year=hoy.year + 1, month=(hoy.month + 2) % 12 or 12, day=1)
        else:
            fecha_limite = hoy.replace(month=hoy.month + 2, day=1)

        # Buscar la primera ocurrencia del día de la semana
        while fecha.weekday() != dias[self.dia]:
            fecha += timedelta(days=1)

        # Saltar la clase de hoy si ya pasó o está por empezar (margen 15 min)
        if fecha == hoy:
            inicio_hoy = timezone.make_aware(datetime.combine(hoy, self.hora_inicio))
            if ahora >= inicio_hoy - timedelta(minutes=15):
                fecha += timedelta(days=7)

        inscripciones_activas = self.turno.inscripcion_set.filter(estado='ACTIVA').select_related('user')
        reservas_a_crear = []
        while fecha < fecha_limite:
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
            reserva.devolver_pago()

    def se_superponen(self, otraClase):
        if self.dia != otraClase.dia:
            return False
        return not (self.hora_fin <= otraClase.hora_inicio or self.hora_inicio >= otraClase.hora_fin)

class ClaseProgramada(models.Model):
    clase = models.ForeignKey(Clase, on_delete=models.CASCADE)
    fecha = models.DateField()
    class Meta:
        ordering = ['fecha', 'clase__hora_inicio']
        unique_together = ('clase', 'fecha')

    def dia(self):
        dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        return dias[self.fecha.weekday()]

    def cupo_actual(self):
        """Cuenta reservas que ocupan cupo: ACTIVA (pagada 100%) y PENDIENTE_PAGO (señada)."""
        return self.reserva_set.filter(estado__in=['ACTIVA', 'PENDIENTE_PAGO']).count()
    
    @property
    def ya_empezo(self):
        from datetime import datetime
        fecha_hora_inicio = datetime.combine(self.fecha, self.clase.hora_inicio)
        fecha_hora_inicio_aware = timezone.make_aware(fecha_hora_inicio)
        return timezone.now() > fecha_hora_inicio_aware

    @property
    def ya_finalizo(self):
        from datetime import datetime
        fecha_hora_fin = datetime.combine(self.fecha, self.clase.hora_fin)
        fecha_hora_fin_aware = timezone.make_aware(fecha_hora_fin)
        return timezone.now() > fecha_hora_fin_aware

    @property
    def puede_pasar_presente(self):
        from datetime import datetime, timedelta
        margen = 15
        
        ahora = timezone.now()
        margen_antes = datetime.combine(self.fecha, self.clase.hora_inicio)
        margen_antes = timezone.make_aware(margen_antes) - timedelta(minutes=margen)
        margen_despues = datetime.combine(self.fecha, self.clase.hora_inicio)
        margen_despues = timezone.make_aware(margen_despues) + timedelta(minutes=margen)

        return margen_antes <= ahora and ahora <= margen_despues

    @property
    def puede_reservarse(self):
        from datetime import datetime, timedelta
        inicio = timezone.make_aware(datetime.combine(self.fecha, self.clase.hora_inicio))
        return timezone.localtime() <= inicio - timedelta(minutes=5)
    
    def cancelar(self, informar = False, motivo = ''):
        from reservas.models import EstadoReserva
        reservas_activas = self.reserva_set.filter(estado=EstadoReserva.ACTIVA)
        for reserva in reservas_activas:
            reserva.desactivar(informar, motivo)

    def se_superponen(self, otraClase):
        return(self.fecha == otraClase.fecha and self.clase.se_superponen(otraClase.clase))
