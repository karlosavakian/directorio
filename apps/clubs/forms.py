from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Reseña
from . import models
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Usuario",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label="Contraseña",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
 
class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField(label='Correo electrónico', required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': 'Nombre de usuario',
            'email': 'Correo electrónico',
        }
        help_texts = {
            'username': None,
            'password1': None,
            'password2': None,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = 'Contraseña'
        self.fields['password2'].label = 'Confirmar contraseña'

 

class ReseñaForm(forms.ModelForm):
    comentario = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
        min_length=200,
        required=True,
        error_messages={
            'required': 'Este campo es obligatorio.',
            'min_length': 'El comentario debe tener al menos 200 caracteres.'
        },
    )

    class Meta:
        model = Reseña
        exclude = ('usuario', 'club', 'creado')

        fields = [
            'instalaciones',
            'entrenadores',
            'ambiente',
            'calidad_precio',
            'variedad_clases',
            'comentario'
        ]
        labels = {
            'instalaciones': 'Instalaciones (limpieza, equipamiento, vestuarios)',
            'entrenadores': 'Entrenadores (trato, conocimientos, motivación)',
            'ambiente': 'Ambiente (compañerismo, nivel de exigencia)',
            'calidad_precio': 'Relación calidad-precio',
            'variedad_clases': 'Variedad de clases (boxeo, técnico, físico, etc.)',
            'comentario': '¿Qué te ha gustado o qué mejorarías del club?'
        }
        
        widgets = {
            'instalaciones': forms.NumberInput(attrs={'min': 1, 'max': 5, 'class': 'star-input', 'required': 'required'}),
            'entrenadores': forms.NumberInput(attrs={'min': 1, 'max': 5, 'class': 'star-input', 'required': 'required'}),
            'ambiente': forms.NumberInput(attrs={'min': 1, 'max': 5, 'class': 'star-input', 'required': 'required'}),
            'calidad_precio': forms.NumberInput(attrs={'min': 1, 'max': 5, 'class': 'star-input', 'required': 'required'}),
            'variedad_clases': forms.NumberInput(attrs={'min': 1, 'max': 5, 'class': 'star-input', 'required': 'required'}),
        }
class ClubPostForm(forms.ModelForm):
    class Meta:
        model = models.ClubPost
        fields = ['titulo', 'contenido', 'evento_fecha']
        widgets = {
            'evento_fecha': forms.DateInput(attrs={'type': 'date'})
        }


class BookingForm(forms.ModelForm):
    class Meta:
        model = models.Booking
        fields = []


class CancelBookingForm(forms.Form):
    """Simple form used to confirm cancellation."""
    pass

