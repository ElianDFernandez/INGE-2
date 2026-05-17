from django import forms
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

class ClaseForm(forms.ModelForm):
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
    
        return cleaned_data