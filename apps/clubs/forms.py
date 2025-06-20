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
    titulo = forms.CharField(
        label='Título',
        max_length=100,
        error_messages={'required': 'Este campo es obligatorio.'}
    )
    comentario = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'minlength': 200}),
        min_length=200,
        required=True,
        error_messages={
            'required': 'Este campo es obligatorio.',
            'min_length': 'El comentario debe tener al menos 200 caracteres.'
        },
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        required_msg = 'Debes puntuar esta categoría.'
        for field in ['instalaciones', 'entrenadores', 'ambiente', 'calidad_precio', 'variedad_clases']:
            self.fields[field].error_messages['required'] = required_msg

    class Meta:
        model = Reseña
        exclude = ('usuario', 'club', 'creado')

        fields = [
            'titulo',
            'instalaciones',
            'entrenadores',
            'ambiente',
            'calidad_precio',
            'variedad_clases',
            'comentario'
        ]
        labels = {
            'titulo': 'Título de la reseña',
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
        fields = ['titulo', 'contenido', 'image', 'evento_fecha']
        widgets = {
            'evento_fecha': forms.DateInput(attrs={'type': 'date'})
        }

class ClubPostReplyForm(forms.ModelForm):
    class Meta:
        model = models.ClubPost
        fields = ['contenido']


class BookingForm(forms.ModelForm):
    class Meta:
        model = models.Booking
        fields = []


class ClubForm(forms.ModelForm):
    class Meta:
        model = models.Club
        exclude = ('slug', 'created_at', 'updated_at', 'verified')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            css = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = (css + ' form-control').strip()
            if isinstance(field.widget, (forms.TextInput, forms.EmailInput,
                                        forms.URLInput, forms.NumberInput,
                                        forms.PasswordInput, forms.Textarea,
                                        forms.DateInput, forms.TimeInput)):
                field.widget.attrs.setdefault('placeholder', ' ')

                  # hide logo input to use dropzone preview
        logo_widget = self.fields.get('logo')
        if logo_widget:
            css = logo_widget.widget.attrs.get('class', '')
            logo_widget.widget.attrs['class'] = (css + ' d-none').strip()


class ClaseForm(forms.ModelForm):
    class Meta:
        model = models.Clase
        fields = ['nombre', 'hora_inicio', 'hora_fin']
        widgets = {
            'hora_inicio': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
            'hora_fin': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
        }


class CancelBookingForm(forms.Form):
    """Simple form used to confirm cancellation."""
    pass


class ClubPhotoForm(forms.ModelForm):
    class Meta:
        model = models.ClubPhoto
        fields = ['image']


class HorarioForm(forms.ModelForm):
    class Meta:
        model = models.Horario
        fields = ['dia', 'hora_inicio', 'hora_fin']
        widgets = {
            'hora_inicio': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
            'hora_fin': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
        }


class CompetidorForm(forms.ModelForm):
    class Meta:
        model = models.Competidor
        fields = [
            'avatar',
            'nombre',
            'record',
            'modalidad',
            'peso',
            'sexo',
            'palmares',
        ]


class EntrenadorForm(forms.ModelForm):
    class Meta:
        model = models.Entrenador
        exclude = ['slug', 'club']

