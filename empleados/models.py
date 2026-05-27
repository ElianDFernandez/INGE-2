from django.db import models
from django.contrib.auth.models import User, UserManager

class EmpleadoManager(UserManager):
	def get_queryset(self):
		return super().get_queryset().filter(is_staff=True)


from actividades.models import Actividad

class Empleado(User):
	objects = EmpleadoManager()

	class Meta:
		proxy = True
		verbose_name = 'Empleado'
		verbose_name_plural = 'Empleados'

	def asignar_actividad(self, actividad_id):
		actividad = Actividad.objects.get(pk=actividad_id)
		EmpleadoActividad.objects.get_or_create(empleado=self, actividad=actividad)

	def eliminar_actividad(self, actividad_id):
		actividad = Actividad.objects.get(pk=actividad_id)
		EmpleadoActividad.objects.filter(empleado=self, actividad=actividad).delete()

	def obtener_actividades(self):
		return Actividad.objects.filter(empleadoactividad__empleado=self)

	def get_contexto_home(self):
		return {}


# Modelo intermedio para asignar actividades a empleados
class EmpleadoActividad(models.Model):
	empleado = models.ForeignKey(User, on_delete=models.CASCADE)
	actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE)

	class Meta:
		unique_together = ('empleado', 'actividad')
		verbose_name = 'Actividad de Empleado'
		verbose_name_plural = 'Actividades de Empleados'
    
    