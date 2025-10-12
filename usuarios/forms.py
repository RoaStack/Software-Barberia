from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class RegistroForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa una contraseña'}),
        label="Contraseña",
        min_length=6,
        error_messages={
            'required': 'Por favor ingresa una contraseña.',
            'min_length': 'La contraseña debe tener al menos 6 caracteres.'
        }
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirma tu contraseña'}),
        label="Confirmar Contraseña",
        error_messages={'required': 'Por favor confirma tu contraseña.'}
    )

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password"]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu nombre'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu apellido'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'}),
        }
        error_messages = {
            'username': {'required': 'El nombre de usuario es obligatorio.'},
            'first_name': {'required': 'El nombre es obligatorio.'},
            'last_name': {'required': 'El apellido es obligatorio.'},
            'email': {'required': 'El correo electrónico es obligatorio.', 'invalid': 'Ingresa un correo válido.'},
        }

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise ValidationError("Este nombre de usuario ya está en uso.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Este correo electrónico ya está registrado.")
        return email

    def clean(self):
        cleaned = super().clean()
        password = cleaned.get("password")
        password_confirm = cleaned.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise ValidationError("Las contraseñas no coinciden.")
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
