from django import forms
from reservas.models import Reserva
from reservas.models import EstadoReserva, Inscripcion

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = []

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.clase_programada = kwargs.pop('clase_programada')
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        if Reserva.objects.filter(user=self.user, clase_programada=self.clase_programada, estado=EstadoReserva.ACTIVA).exists():
            raise forms.ValidationError('Ya tenés una reserva para esta clase.')

        if (self.clase_programada.cupo_actual() >= self.clase_programada.clase.cupo_maximo):
            raise forms.ValidationError('No hay cupos disponibles para esta clase.')

        return cleaned_data
    
class ReservaCancelForm(forms.Form):
    class meta: 
        model = Reserva
        fields = []

        def clean(self):
            cleaned_data = super().clean()

            if self.instance.estado != EstadoReserva.ACTIVA:
                raise forms.ValidationError('La reserva ya está cancelada.')
            
            return cleaned_data

class InscripcionForm(forms.ModelForm):
    class Meta:
        model = Inscripcion
        fields = []

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.turno = kwargs.pop('turno')
        
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        if Inscripcion.objects.filter(user=self.user, turno=self.turno, estado='ACTIVA').exists():
            raise forms.ValidationError('Ya estás inscripto en este turno.')

        return cleaned_data
    
class InscripcionCancelForm(forms.Form):
    class meta:
        model = Inscripcion
        fields = []
        
        def clean(self):
            cleaned_data = super().clean()

            if self.instance and self.instance.estado != 'ACTIVA':
                raise forms.ValidationError('La inscripción ya está cancelada.')

            return cleaned_data