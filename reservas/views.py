from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect

from actividades.models import Actividad
from turnos.models import Clase, ClaseProgramada
from reservas.forms import ReservaForm

def clases_disponibles(request):
    for clase in Clase.objects.all():
        for i in range(14): 
            fecha = timezone.localdate() + timedelta(days=i)
            if fecha.weekday() == clase.dia_numero():
                # si no existía la creo
                ClaseProgramada.objects.get_or_create(clase=clase, fecha=fecha) 
    
    actividades = Actividad.objects.prefetch_related('turno_set__clase_set')
    return render(request, 'clases_disponibles.html', {'actividades': actividades})


def reserva_confirm(request, clase_programada_pk):
    clase_programada = get_object_or_404(ClaseProgramada, pk=clase_programada_pk)

    if request.method == 'POST':
        form = ReservaForm(request.POST, user=request.user, clase_programada=clase_programada)

        if form.is_valid():
            reserva = form.save(commit=False)

            reserva.user = request.user
            reserva.clase_programada = clase_programada

            reserva.save()
            return redirect('clases_disponibles')

    else:
        form = ReservaForm(user=request.user, clase_programada=clase_programada)

    return render(request, 'reserva_confirm.html', {'form': form, 'clase_programada': clase_programada})