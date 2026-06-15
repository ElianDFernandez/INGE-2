from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ListaEspera,EstadoListaEspera 
from django.shortcuts import render, get_object_or_404, redirect
from turnos.models import ClaseProgramada

@login_required
def inscribirse_lista_espera(request, clase_programada_pk):
    clase_programada = get_object_or_404(ClaseProgramada, pk=clase_programada_pk)

    if request.method == 'POST':
        ListaEspera.objects.get_or_create(
            user=request.user,
            clase_programada=clase_programada,
        )
        messages.success(request, 'Te anotaste en la lista de espera.')
        return redirect('reservas_disponibles')
    return render(request, 'lista_espera/confirmar_inscripcion_lista.html', {'clase_programada': clase_programada})



@login_required
def cancelar_lista_espera(request, clase_programada_pk):
    entrada = ListaEspera.objects.filter(user=request.user, clase_programada_id=clase_programada_pk,estado=
    EstadoListaEspera.PENDIENTE).first()


    if request.method == 'POST':
        entrada.estado = EstadoListaEspera.CANCELADO
        entrada.save()
        messages.success(request, 'Saliste de la lista de espera.')
        
    return redirect('reservas_disponibles')

