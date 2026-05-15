from django.db import models

# Create your models here.
class DiaSemana(models.TextChoices):
    LUNES = 'LUNES', 'Lunes'
    MARTES = 'MARTES', 'Martes'
    MIERCOLES = 'MIERCOLES', 'Miércoles'
    JUEVES = 'JUEVES', 'Jueves'
    VIERNES = 'VIERNES', 'Viernes'
    SABADO = 'SABADO', 'Sábado'
    DOMINGO = 'DOMINGO', 'Domingo'


class Turno(models.Model):
    nombre = models.CharField(max_length=100)

class Clase(models.Model):
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE)
    dia_semana = models.CharField(max_length=10, choices=DiaSemana.choices)
    costo = models.DecimalField(max_digits=6, decimal_places=2)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

