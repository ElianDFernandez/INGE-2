from django.db import models

# Definimos las 4 disciplinas permitidas
DISCIPLINAS_CHOICES = [
    ('VOLEY', 'Vóley'),
    ('FUTBOL', 'Fútbol 5'),
    ('BASQUET', 'Básquet'),
    ('PADEL', 'Pádel'),
]

class Actividad(models.Model):
    nombre = models.CharField(max_length=20, choices=DISCIPLINAS_CHOICES)

    def __str__(self):
        return self.get_nombre_display()
