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
            # Regla de negocio: inicia pendiente de pago
            reserva.estado = 'PENDIENTE_PAGO' 
            reserva.pago_confirmado = False
            reserva.save()
            
            # 2. Regla de negocio: Calcular el 50% de la seña

            valor_total = float(clase_programada.clase.costo)
            valor_sena = valor_total * 0.50
            
            # 3. Integración con Mercado Pago
            sdk = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)

            url_exito = request.build_absolute_uri(reverse('pago_exitoso', args=[reserva.id]))
            url_fallo = request.build_absolute_uri(reverse('pago_fallido', args=[reserva.id]))

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
                # "auto_return": "approved",
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
    reserva = get_object_or_404(Reserva, id=reserva_id, user=request.user)
    
    payment_id = request.GET.get('payment_id')
    
    # Confirma reserva
    reserva.estado = EstadoReserva.ACTIVA
    reserva.pago_confirmado = True
    reserva.mp_payment_id = payment_id
    reserva.save()
    
    # Nota: restar cupo donde?
    
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
    reservas = Reserva.objects.filter(user=request.user).select_related('clase_programada__clase__turno__actividad').order_by('clase_programada__fecha', 'clase_programada__clase__hora_inicio')
    inscripciones = Inscripcion.objects.filter(user=request.user)
    return render(request, 'reservas/reserva_list.html', {
        'reservas': reservas, 
        'inscripciones': inscripciones
    })

@login_required
def reserva_cancel(request, reserva_pk):
    reserva = get_object_or_404(Reserva, pk=reserva_pk, user=request.user, estado='ACTIVA')

    if request.method == 'POST':
        form = ReservaCancelForm(request.POST)
        if form.is_valid():
            reserva.estado = EstadoReserva.CANCELADA
            reserva.fecha_cancelacion = timezone.now()
            reserva.save()
            return redirect('reserva_list')
    else:
        form = ReservaCancelForm()

    return render(request, 'reservas/reserva_cancel.html', {'form': form, 'reserva': reserva})

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
            inscripcion.estado = 'DE_BAJA'
            inscripcion.fecha_baja = timezone.now()
            inscripcion.save()

            inscripcion.cancelar_clases_programadas()
            return redirect('reserva_list')
    else:
        form = InscripcionCancelForm()

    return render(request, 'inscripciones/inscripcion_cancel.html', {
        'form': form,
        'inscripcion': inscripcion,
        'clases_a_cancelar': clases_a_cancelar
    })

