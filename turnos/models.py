from django.db import models
from actividades.models import Actividad

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


class Clase(models.Model):
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE)
    dia = models.CharField(max_length=10, choices=DiaSemana.choices)
    espacio = models.CharField(max_length=20, choices=Espacio.choices)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    costo = models.DecimalField(max_digits=6, decimal_places=2)
    cupo_maximo = models.PositiveIntegerField()

