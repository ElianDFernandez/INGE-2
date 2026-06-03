from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

# Formulario de Registro
class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Correo electrónico", help_text="Requerido. Ingresá una dirección de correo válida.")

    class Meta:
        model = User
        fields = ("username", "email")

    def clean_email(self):
        email_ingresado = self.cleaned_data.get('email').lower()
        if User.objects.filter(email=email_ingresado).exists():
            raise forms.ValidationError('Este email ya esta en uso.')
            
        return email_ingresado

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

# Formulario de Login
class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Correo electrónico", widget=forms.TextInput(attrs={'autofocus': True}))

# Formulario edicion de perfil
class PerfilForm(forms.ModelForm):
    email = forms.EmailField(
        required=True, 
        error_messages={'required': 'Por favor, no te olvides de poner tu email.'}
    )
    current_password = forms.CharField(required=False)
    new_password = forms.CharField(required=False, min_length=8)
    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_email(self):
        email_ingresado = self.cleaned_data.get('email').lower()
        usuario_actual = self.instance 
        if User.objects.filter(email=email_ingresado).exclude(pk=usuario_actual.pk).exists():
            raise forms.ValidationError('Este email ya esta en uso.')
            
        return email_ingresado

    def clean(self):
        datos = super().clean()
        clave_vieja = datos.get('current_password')
        clave_nueva = datos.get('new_password')
        if clave_nueva:
            if not clave_vieja:
                self.add_error('current_password', 'Necesitas escribir tu clave actual para poder cambiarla.')
            elif not self.instance.check_password(clave_vieja):
                self.add_error('current_password', 'Clave actual incorrecta.')
        return datos

    def save(self, commit=True):
        usuario = super().save(commit=False)
        clave_nueva = self.cleaned_data.get('new_password')
        if clave_nueva:
            usuario.set_password(clave_nueva)
        if commit:
            usuario.save()
            
        return usuario