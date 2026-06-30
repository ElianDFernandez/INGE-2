from datetime import datetime, timedelta
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Prefetch
from django.contrib import messages
from django.urls import reverse
import mercadopago
from django.conf import settings

from .models import Reserva, EstadoReserva, Inscripcion
from .forms import ReservaCancelForm, ReservaForm, InscripcionCancelForm, InscripcionForm

from actividades.models import Actividad
from turnos.models import Turno, Clase, ClaseProgramada


@login_required
def reservas_disponibles(request):
    hoy = timezone.localdate()
    # CLASES INDIVIDUALES
    clases_programadas = ClaseProgramada.objects.filter(fecha__gte=hoy, clase__activo=True, clase__turno__activo=True).select_related('clase', 'clase__turno', 'clase__turno__actividad').order_by('fecha', 'clase__hora_inicio')
    clases_reservadas_ids = Reserva.objects.filter(user=request.user, estado=EstadoReserva.ACTIVA).values_list('clase_programada_id', flat=True)
    # TURNOS
    turnos = Turno.objects.filter(activo=True).select_related('actividad').prefetch_related(
        Prefetch('clase_set', queryset=Clase.objects.filter(activo=True).order_by('dia', 'hora_inicio').prefetch_related(
            Prefetch('claseprogramada_set', queryset=ClaseProgramada.objects.filter(fecha__gte=hoy).order_by('fecha'))
        ))
    )
    for turno in turnos:
        turno.usuario_inscripto = turno.esta_inscripto(request.user)

    actividades_filtro = Actividad.objects.all().order_by('nombre')

    inscripciones_ids = Inscripcion.objects.filter(
        user=request.user,
        estado='ACTIVA'
    ).values_list('turno_id', flat=True)

    return render(request, 'reservas_disponibles.html', {
        'clases_programadas': clases_programadas,
        'clases_reservadas_ids': list(clases_reservadas_ids),
        'turnos': turnos,
        'inscripciones_ids': list(inscripciones_ids),
        'actividades_filtro': actividades_filtro
    })

@login_required
def reserva_confirm(request, clase_programada_pk):
    clase_programada = get_object_or_404(ClaseProgramada, pk=clase_programada_pk, clase__activo=True, clase__turno__activo=True)
    
    if request.method == 'POST':
        form = ReservaForm(request.POST, user=request.user, clase_programada=clase_programada)
        if form.is_valid():
            # 1. Crea la reserva sin guardarla definitivamente para ajustar el estado
            reserva = form.save(commit=False)
            reserva.user = request.user
            reserva.clase_programada = clase_programada
            # Regla de negocio: comienza iniciada
            reserva.estado = 'INICIADA' 
            reserva.pago_confirmado = False
            reserva.save()
            
            # 2. Regla de negocio: Calcular el 50% de la seña

            valor_total = float(clase_programada.clase.costo)
            valor_sena = valor_total * 0.50
            
            # 3. Integración con Mercado Pago
            sdk = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)

            url_ngrok = "https://proven-energize-freckled.ngrok-free.dev"

            url_exito = f"{url_ngrok}/reservas/reserva/{reserva.id}/pago-exitoso/"
            url_fallo = f"{url_ngrok}/reservas/reserva/{reserva.id}/pago-fallido/"

            preference_data = {
                "items": [
                    {
                        "title": f"Seña Reserva: {clase_programada.clase.turno.actividad.nombre}",
                        "quantity": 1,
                        "unit_price": float(valor_sena),
                    }
                ],
                "back_urls": {
                    "success": url_exito,
                    "failure": url_fallo,
                    "pending": url_fallo
                },
                "auto_return": "approved",
            }
           
            try:
                preference_response = sdk.preference().create(preference_data)
                print(">>> RESPUESTA CRUDA DE MP:", preference_response)
                preference = preference_response["response"]
                
                reserva.mp_preference_id = preference['id']
                reserva.save()
                
                # Redirige a MP
                return redirect(preference['sandbox_init_point']) 

            except Exception as e:
                print(">>> ERROR EN PYTHON:", e)
                reserva.delete() # Limpiamos la base de datos si falló la conexión
                messages.error(request, 'Error en el pago de la seña. No se ha podido establecer la conexión. Intente más tarde.')
                return redirect('reservas_disponibles')
    else:
        form = ReservaForm(user=request.user, clase_programada=clase_programada)

    return render(request, 'reservas/reserva_confirm.html', {'form': form, 'clase_programada': clase_programada})

@login_required
def pago_exitoso(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    payment_id = request.GET.get('payment_id')
    
    if payment_id:
        reserva.mp_payment_id = payment_id
        
        # ESCENARIO 1: Acaba de pagar la seña (el primer 50%)
        if reserva.estado == 'INICIADA':
            reserva.estado = 'PENDIENTE_PAGO'
            
        # ESCENARIO 2: Acaba de pagar el restante (el segundo 50%)
        elif reserva.estado == 'PENDIENTE_PAGO':
            reserva.estado = 'ACTIVA'
            reserva.pago_confirmado = True # Pagó el 100%
            
        reserva.save()
        #Nota : restar cupo donde?
    
    messages.success(request, 'La operación se realizó correctamente. Tu reserva está confirmada.')
    return redirect('reserva_list')

@login_required
def pago_fallido(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id, user=request.user)
    
    # Cancela reserva por falta de pago
    reserva.estado = EstadoReserva.CANCELADA
    reserva.save()
    
    messages.error(request, 'El pago no pudo procesarse. Tu reserva ha sido cancelada.')
    return redirect('reserva_list')

@login_required
def reserva_list(request):
    hoy = timezone.localdate()
    reservas = Reserva.objects.filter(user=request.user).select_related('clase_programada__clase__turno__actividad').order_by('clase_programada__fecha', 'clase_programada__clase__hora_inicio').exclude(estado='INICIADA')
    inscripciones = Inscripcion.objects.filter(user=request.user)
    return render(request, 'reservas/reserva_list.html', {
        'reservas': reservas, 
        'inscripciones': inscripciones
    })

@login_required
def reserva_cancel(request, reserva_pk):
    reserva = get_object_or_404(Reserva, pk=reserva_pk, user=request.user, estado='ACTIVA')

    # Determina si es abonado (inscripto al turno de esta clase)
    turno = reserva.clase_programada.clase.turno
    es_abonado = Inscripcion.objects.filter(
        user=request.user, turno=turno, estado='ACTIVA'
    ).exists()

    # Calcular anticipación para saber qué pasará
    ahora = timezone.now()
    fecha_hora_clase = datetime.combine(
        reserva.clase_programada.fecha,
        reserva.clase_programada.clase.hora_inicio
    )
    fecha_hora_clase = timezone.make_aware(fecha_hora_clase, timezone.get_current_timezone())
    anticipacion = fecha_hora_clase - ahora

    if es_abonado:
        if reserva.pago_confirmado and anticipacion >= timedelta(hours=48):
            resultado_cancelacion = 'vale'
        elif reserva.pago_confirmado:
            resultado_cancelacion = 'pierde'
        else:
            resultado_cancelacion = 'sin_pago'
    else:
        if reserva.pago_confirmado and anticipacion >= timedelta(hours=24):
            resultado_cancelacion = 'devuelve_sena'
        elif reserva.pago_confirmado:
            resultado_cancelacion = 'pierde_sena'
        else:
            resultado_cancelacion = 'sin_pago'

    if request.method == 'POST':
        form = ReservaCancelForm(request.POST)
        if form.is_valid():
            reserva.estado = EstadoReserva.CANCELADA
            reserva.fecha_cancelacion = ahora
            reserva.save()

            if resultado_cancelacion == 'vale':
                from socios.models import Vale
                import calendar as cal
                hoy = timezone.localdate()
                _, ultimo_dia = cal.monthrange(hoy.year, hoy.month)
                Vale.objects.create(
                    socio_id=request.user.id,
                    actividad=turno.actividad,
                    fecha_vencimiento=hoy.replace(day=ultimo_dia)
                )
                reserva.sena_devuelta = True
                messages.success(request, 'Clase cancelada. Se generó un vale para la actividad.')
            elif resultado_cancelacion == 'pierde':
                messages.warning(request, 'Clase cancelada. No se genera vale por cancelar con menos de 48hs de anticipación.')
            elif resultado_cancelacion == 'devuelve_sena':
                reserva.devolver_pago()
                return redirect('simular_reembolso', reserva_pk=reserva.pk)
            elif resultado_cancelacion == 'pierde_sena':
                messages.warning(request, 'Reserva cancelada. La seña se pierde por cancelar con menos de 24hs de anticipación.')
            else:
                messages.success(request, 'Reserva cancelada correctamente.')

            reserva.save()
            return redirect('reserva_list')
    else:
        form = ReservaCancelForm()

    return render(request, 'reservas/reserva_cancel.html', {
        'form': form,
        'reserva': reserva,
        'es_abonado': es_abonado,
        'resultado_cancelacion': resultado_cancelacion,
    })

@login_required
def inscripcion_confirm(request, turno_pk):
    turno = get_object_or_404(Turno, pk=turno_pk, activo=True)
    clases = turno.get_clases_programadas().filter(fecha__gte=timezone.localdate()).exclude(
        reserva__user = request.user,
        reserva__estado = EstadoReserva.ACTIVA
    )

    if request.method == 'POST':
        form = InscripcionForm(request.POST, user=request.user, turno=turno)

        if form.is_valid():
            inscripcion = form.save(commit=False)
            inscripcion.user = request.user
            inscripcion.turno = turno
            inscripcion.save()
            inscripcion.reservar_clases_programadas()
            messages.success(request, f'¡Genial! Te inscribiste con éxito al turno {turno.nombre} de {turno.actividad.nombre}.')
            return redirect('reservas_disponibles')
    else:
        form = InscripcionForm(user=request.user, turno=turno)

    return render(request, 'inscripciones/inscripcion_confirm.html', {
        'form': form,
        'turno': turno,
        'clases_a_reservar': clases
    })

@login_required
def inscripcion_cancel(request, inscripcion_pk):
    inscripcion = get_object_or_404(Inscripcion, pk=inscripcion_pk, user=request.user, estado='ACTIVA')
    # muestro que clases se cancelarían si se cancela la inscripcion al turno (solo las activas)
    clases_a_cancelar = inscripcion.turno.get_clases_programadas().filter(
        fecha__gte=timezone.localdate(),
        reserva__user=request.user,
        reserva__estado=EstadoReserva.ACTIVA
    )

    if request.method == 'POST':
        form = InscripcionCancelForm(request.POST)
        if form.is_valid():
            vales_generados = inscripcion.cancelar()

            if vales_generados > 0:
                messages.success(request, f'Inscripción cancelada. Se generaron {vales_generados} vale{"s" if vales_generados > 1 else ""} para {inscripcion.turno.actividad.nombre}.')
            else:
                messages.success(request, 'Inscripción cancelada correctamente.')
            return redirect('reserva_list')
    else:
        form = InscripcionCancelForm()

    return render(request, 'inscripciones/inscripcion_cancel.html', {
        'form': form,
        'inscripcion': inscripcion,
        'clases_a_cancelar': clases_a_cancelar
    })

@login_required
def simular_reembolso(request, reserva_pk):
    """Simula una pantalla de devolución de MercadoPago."""
    reserva = get_object_or_404(
        Reserva.objects.select_related('clase_programada__clase__turno__actividad'),
        pk=reserva_pk,
        user=request.user
    )

    if not reserva.corresponde_devolucion:
        messages.warning(request, 'No corresponde devolución para esta reserva.')
        return redirect('reserva_list')

    monto_devuelto = reserva.clase_programada.clase.costo
    if not reserva.pago_total_confirmado:
        monto_devuelto = monto_devuelto / 2

    return render(request, 'reservas/simular_reembolso.html', {
        'reserva': reserva,
        'monto_devuelto': monto_devuelto,
    })

def pagar_restante(request, reserva_id):
    sdk = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)
    reserva = get_object_or_404(Reserva, id=reserva_id, user=request.user)
    
    # Asegurarnos de que solo se pueda pagar el restante si está en el estado correcto
    if reserva.estado != EstadoReserva.PENDIENTE_PAGO:
        # Si alguien quiere hacer trampa, lo mandamos de vuelta
        return redirect('nombre_de_tu_vista_mis_reservas')

    precio_total = reserva.clase_programada.clase.costo
    valor_restante = float(precio_total) / 2.0 
    
    url_ngrok = "https://proven-energize-freckled.ngrok-free.dev"
    url_exito = f"{url_ngrok}/reservas/reserva/{reserva.id}/pago-exitoso/"
    url_fallo = f"{url_ngrok}/reservas/reserva/{reserva.id}/pago-fallido/"

    preference_data = {
        "items": [
            {
                "title": f"Pago Restante: {reserva.clase_programada.clase.turno.actividad.nombre}",
                "quantity": 1,
                "unit_price": valor_restante,
            }
        ],
        "back_urls": {
            "success": url_exito,
            "failure": url_fallo,
            "pending": url_fallo
        },
        "auto_return": "approved",
    }
    
    preference_response = sdk.preference().create(preference_data)
    preference = preference_response["response"]
    
    return redirect(preference['sandbox_init_point'])
