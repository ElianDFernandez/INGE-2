from django import forms
from .models import Turno, Clase

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
        fields = ['turno', 'hora_inicio', 'hora_fin', 'costo', 'cupo_maximo']
        widgets = {
            'turno': forms.Select(attrs={'class': 'form-select'}),
            'hora_inicio': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'hora_fin': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'costo': forms.NumberInput(attrs={'class': 'form-control', 'type': 'number', 'step': '0.01'}),
            'cupo_maximo': forms.NumberInput(attrs={'class': 'form-control', 'type': 'number'}),
        }