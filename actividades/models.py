from django.db import models

# Create your models here.

from django.db import models

class Actividad(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.FloatField()
    cupo_maximo = models.PositiveIntegerField()

    def __str__(self):
        return self.nombre

class Turno(models.Model):
    DIAS_CHOICES = [
        ('LUN', 'Lunes'),
        ('MAR', 'Martes'),
        ('MIE', 'Miércoles'),
        ('JUE', 'Jueves'),
        ('VIE', 'Viernes'),
        ('SAB', 'Sábado'),
        ('DOM', 'Domingo'),
    ]
    
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE, related_name='turnos')
    dia_semana = models.CharField(max_length=3, choices=DIAS_CHOICES)
    horario_inicio = models.TimeField()
    horario_fin = models.TimeField()
    cupo_disponible = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.actividad.nombre} - {self.get_dia_semana_display()} ({self.horario_inicio})"
