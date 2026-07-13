from celery import shared_task 
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.urls import reverse
from django.utils import timezone 
from datetime import datetime, timedelta 
from .models import ListaEspera, EstadoListaEspera
from django.conf import settings 

@shared_task
def notificar_siguiente(clase_programada_id):
    """Notifica al siguiente socio en la lista de espera"""
    from turnos.models import ClaseProgramada
    
    clase_programada = ClaseProgramada.objects.get(id=clase_programada_id)
    
    # No enviar nuevas notificaciones si la clase comienza en menos de 2 horas.
    fecha_hora_inicio = timezone.make_aware(
        datetime.combine(clase_programada.fecha, clase_programada.clase.hora_inicio)
    )
    if fecha_hora_inicio - timezone.now() < timedelta(hours=2):
        return
    
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
    url_ngrok= "https://ashy-streak-slather.ngrok-free.dev"
    subject = f'¡Cupo disponible en {clase_programada.clase.turno.actividad.nombre}!'
    notificacion_url = f"{url_ngrok.rstrip('/')}" + reverse('confirmar_desde_email', args=[siguiente.id])
    
    html_message = render_to_string('mensaje_confirmacion.html', {
        'titulo': '¡Confirmá o cancelá tu reserva!',
        'usuario': siguiente.user,
        'mensaje': 'Se liberó un cupo en la clase para la que estabas en lista de espera. Podés confirmar tu reserva o cancelar la notificación desde el enlace.',
        'actividad': clase_programada.clase.turno.actividad.nombre,
        'fecha': clase_programada.fecha,
        'hora_inicio': clase_programada.clase.hora_inicio,
        'hora_fin': clase_programada.clase.hora_fin,
        'notificacion_url': notificacion_url,
        'sitio_url': url_ngrok,
    })

    text_message = strip_tags(html_message)

    send_mail(
        subject,
        text_message,
        settings.DEFAULT_FROM_EMAIL,
        [siguiente.user.email],
        html_message=html_message,
        fail_silently=False,
    )
    
    # Programa verificación en 2 horas,para testear vencimientos
    verificar_confirmacion.apply_async(
        args=[siguiente.id],
        countdown=90 #90 segundos para testear, en producción sería 7200 (2 horas)
    )


@shared_task
def verificar_confirmacion(lista_espera_id):
    """Verifica si el socio confirmó en 2 horas"""
    
    entrada = ListaEspera.objects.get(id=lista_espera_id)
    
    
    if entrada.estado == EstadoListaEspera.CONFIRMADO:
        return
    
    # Si aún está notificado (no confirmó)
    if entrada.estado == EstadoListaEspera.NOTIFICADO:
        entrada.estado = EstadoListaEspera.EXPIRADO
        entrada.save()
        

        notificar_siguiente.delay(entrada.clase_programada.id)
