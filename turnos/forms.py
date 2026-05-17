from django import forms

from actividades.models import Actividad
from .models import Turno, Clase


class CreateTurnoForm(forms.ModelForm):
    class Meta:
        model = Turno
        fields = ['nombre', 'actividad']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'actividad': forms.Select(attrs={'class': 'form-select'}),
        }
    
class TurnoForm(forms.ModelForm):
    class Meta:
        model = Turno
        fields = ['nombre', 'actividad']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'actividad': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        nueva_actividad = cleaned_data.get('actividad')

        # no cambie la actividad
        if self.instance.pk and nueva_actividad == self.instance.actividad:
            return cleaned_data

        # turno no existe, no tiene clases
        if not self.instance.pk: 
            return cleaned_data

        # por cada clase mia me fijo si hay alguna clase de la nueva actividad que se solape
        for clase in self.instance.clase_set.all():
            clases = Clase.objects.filter(turno__actividad=nueva_actividad, dia=clase.dia).exclude(turno=self.instance)
            for clase_aux in clases:
                if (clase.hora_inicio < clase_aux.hora_fin and clase.hora_fin > clase_aux.hora_inicio):
                    raise forms.ValidationError('La clase se superpone con otra clase ya existente de la actividad seleccionada.')
        return cleaned_data


class ClaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.actividad = kwargs.pop('actividad', None)
        super().__init__(*args, **kwargs)
    
    class Meta:
        model = Clase
        fields = ['dia', 'espacio', 'hora_inicio', 'hora_fin', 'costo', 'cupo_maximo']
        widgets = {
            'dia': forms.Select(attrs={'class': 'form-select'}),
            'espacio': forms.Select(attrs={'class': 'form-select'}),
            'hora_inicio': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'hora_fin': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'costo': forms.NumberInput(attrs={'class': 'form-control', 'type': 'number', 'step': '0.01'}),
            'cupo_maximo': forms.NumberInput(attrs={'class': 'form-control', 'type': 'number'},),
        }

    def clean(self):
        cleaned_data = super().clean()
        hora_inicio = cleaned_data.get('hora_inicio')
        hora_fin = cleaned_data.get('hora_fin')
        
        if hora_inicio and hora_fin and hora_inicio >= hora_fin:
            raise forms.ValidationError('La hora de inicio debe ser anterior a la hora de fin.')
        
        actividad = self.actividad # viene del turno, no es campo propio
        espacio = cleaned_data.get('espacio')
        dia = cleaned_data.get('dia')

        # no pueden haber clases de la misma actividad que se superpongan en el tiempo
        if actividad and dia and hora_inicio and hora_fin:
            clases = Clase.objects.filter(turno__actividad=actividad, dia=dia).exclude(pk=self.instance.pk)
            print("ENTRA")
            for clase in clases:
                if (hora_inicio < clase.hora_fin and hora_fin > clase.hora_inicio):
                    raise forms.ValidationError('Ya existe una clase de esta actividad durante el horario elegido.')


        # no pueden haber clases en el mismo espacio que se superpongan en el tiempo
        if espacio and dia and hora_inicio and hora_fin:
            clases = Clase.objects.filter(espacio=espacio, dia=dia).exclude(pk=self.instance.pk)

            for clase in clases:
                if (hora_inicio < clase.hora_fin and hora_fin > clase.hora_inicio):
                    raise forms.ValidationError('El espacio seleccionado se encuentra en uso durante el horario elegido.')

        return cleaned_data