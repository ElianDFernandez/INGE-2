from django.db import models


class Actividad(models.Model):
    nombre = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre

    def tiene_reservas(self):
        from reservas.models import Reserva, EstadoReserva

        return Reserva.objects.filter(
            clase_programada__clase__turno__actividad=self
        ).exclude(estado=EstadoReserva.CANCELADA).exists()
