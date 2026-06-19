from celery import shared_task 
from django.core.mail import send_mail
from django.utils import timezone 
from datetime import timedelta 
from .models import ListaEspera,EstadoListaEspera
from django.conf import settings 

@shared_task
def notificar_siguiente(clase_programada_id):
    """Notifica al siguiente socio en la lista de espera"""
    from turnos.models import ClaseProgramada
    
    clase_programada = ClaseProgramada.objects.get(id=clase_programada_id)
    
    # Busca el siguiente pendiente
    siguiente = ListaEspera.objects.filter(
        clase_programada=clase_programada,
        estado=EstadoListaEspera.PENDIENTE
    ).first()
    
    if not siguiente:
        return
    
    # Actualiza estado a notificado
    siguiente.estado = EstadoListaEspera.NOTIFICADO
    siguiente.fecha_notificacion = timezone.now()
    siguiente.save()
    
    # Envía email
    subject = f'¡Cupo disponible en {clase_programada.clase.turno.actividad.nombre}!'
    message = f"""
Hola {siguiente.user.get_full_name()},

Se liberó un cupo en la clase de {clase_programada.clase.turno.actividad.nombre} 
el {clase_programada.fecha} de {clase_programada.clase.hora_inicio} a {clase_programada.clase.hora_fin}.

Tienes 2 horas para confirmar tu reserva.

Saludos,
Centro Deportivo
    """
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [siguiente.user.email],
        fail_silently=False,
    )
    
    # Programa verificación en 2 horas
    verificar_confirmacion.apply_async(
        args=[siguiente.id],
        countdown=7200
    )


@shared_task
def verificar_confirmacion(lista_espera_id):
    """Verifica si el socio confirmó en 2 horas"""
    
    entrada = ListaEspera.objects.get(id=lista_espera_id)
    
    # Si ya confirmó, no hace nada
    if entrada.estado == EstadoListaEspera.CONFIRMADO:
        return
    
    # Si aún está notificado (no confirmó)
    if entrada.estado == EstadoListaEspera.NOTIFICADO:
        entrada.estado = EstadoListaEspera.EXPIRADO
        entrada.save()
        
        # Notificar al siguiente
        notificar_siguiente.delay(entrada.clase_programada.id)
