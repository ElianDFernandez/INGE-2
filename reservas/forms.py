from django import forms
from reservas.models import Reserva
from reservas.models import EstadoReserva

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

        if Reserva.objects.filter(user=self.user, 
                                  clase_programada=self.clase_programada, 
                                  estado=EstadoReserva.ACTIVA).exists():
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