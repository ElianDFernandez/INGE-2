from django import forms
from .models import Actividad


class ActividadForm(forms.ModelForm):
    class Meta:
        model = Actividad
        fields = ['nombre']
        widgets = {
            'nombre': forms.Select(attrs={'class': 'form-select'}),
        }

