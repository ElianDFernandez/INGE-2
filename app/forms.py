from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

# Formulario de Registro
class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Correo electrónico", help_text="Requerido. Ingresá una dirección de correo válida.")

    class Meta:
        model = User
        fields = ("username", "email")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

# Formulario de Login
class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Correo electrónico", widget=forms.TextInput(attrs={'autofocus': True}))