from django import forms
from .models import Actividad


class ActividadForm(forms.ModelForm):
    class Meta:
        model = Actividad
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_nombre(self):
        nombre_ingresado = self.cleaned_data.get('nombre').strip()
        if Actividad.objects.filter(nombre__iexact=nombre_ingresado).exists():
            raise forms.ValidationError('Esta actividad ya existe.')
        return nombre_ingresado
    