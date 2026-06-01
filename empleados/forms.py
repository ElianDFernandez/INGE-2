from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail


class EmpleadoCreateForm(forms.ModelForm):
    email = forms.EmailField(required=True, label="Correo electrónico")

    class Meta:
        model = User
        fields = ("username", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.is_staff = True
        user.set_password(user.email)  # La contraseña temporal es el email del empleado
        if commit:
            user.save()
            send_mail(
                subject="Tu cuenta de empleado",
                message=(
                    "Se creo tu cuenta de empleado.\n"
                    f"Usuario: {user.email}\n"
                    f"Contraseña temporal: {user.email}\n"
                    "Deberas cambiarla al iniciar sesion."
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=True,
            )
        return user

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email ya esta en uso.")
        return email


class EmpleadoUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True, label="Correo electrónico")

    class Meta:
        model = User
        fields = ("username", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.is_staff = True
        if commit:
            user.save()
        return user

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Este email ya esta en uso.")
        return email