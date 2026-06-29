from django.db import models
from django.contrib.auth.models import User
from turnos.models import ClaseProgramada

# Create your models here.
class EstadoListaEspera (models.TextChoices): 
    PENDIENTE = 'pendiente', 'Pendiente'
    CONFIRMADO = 'confirmado', 'Confirmado'
    CANCELADO = 'cancelado', 'Cancelado'
    NOTIFICADO = 'notificado', 'Notificado'
    EXPIRADO = 'expirado', 'Expirado'
    
class ListaEspera (models.Model) :
    user = models.ForeignKey(User , on_delete=models.CASCADE, related_name='lista_espera')
    clase_programada = models.ForeignKey(ClaseProgramada, on_delete=models.CASCADE,related_name='lista_espera')
    fecha_anotacion = models.DateTimeField(auto_now_add=True) #Atributo para la fifo de lista de espera
    fecha_notificacion = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=EstadoListaEspera.choices, default=EstadoListaEspera.PENDIENTE)
     
    class Meta: 
        ordering = ['fecha_anotacion']
        unique_together = ['user', 'clase_programada'] 
    def __str__(self):
        return f"{self.user} - {self.clase_programada} ({self.estado})"
    