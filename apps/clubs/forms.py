from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Reseña
from . import models
from .countries import COUNTRY_CHOICES
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
    """Formulario para crear publicaciones de club."""

    class Meta:
        model = models.ClubPost
        # Eliminamos los campos de título y fecha del formulario público
        fields = ['contenido', 'image']
        widgets = {
            'contenido': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': '¿Qué está pasando?'
                }
            ),
            # Ocultamos el input real y se activará desde un icono
            'image': forms.ClearableFileInput(attrs={'class': 'd-none'})
        }

class ClubPostReplyForm(forms.ModelForm):
    class Meta:
        model = models.ClubPost
        fields = ['contenido']
        widgets = {
            'contenido': forms.TextInput(attrs={
                'placeholder': 'Escribe una respuesta...',
                'class': 'form-control form-control-sm'
            })
        }


class BookingForm(forms.ModelForm):
    class Meta:
        model = models.Booking
        fields = []

 

class BookingClassForm(forms.ModelForm):
    class Meta:
        model = models.BookingClass
        fields = ['titulo', 'precio', 'duracion', 'detalle', 'destacado']
        widgets = {
            'detalle': forms.Textarea(attrs={
                'rows': 2,
                'maxlength': 400,  # HTML5
                'class': 'form-control',  # se asegura en __init__
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            css = field.widget.attrs.get('class', '')
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = (css + ' form-control').strip()
            if isinstance(field.widget, (
                forms.TextInput,
                forms.EmailInput,
                forms.URLInput,
                forms.NumberInput,
                forms.PasswordInput,
                forms.Textarea,
                forms.DateInput,
                forms.TimeInput,
            )):
                field.widget.attrs.setdefault('placeholder', ' ')


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

        about_field = self.fields.get('about')
        if about_field:
            about_field.label = 'Bio'

                  # hide logo input to use dropzone preview
        logo_widget = self.fields.get('logo')
        if logo_widget:
            css = logo_widget.widget.attrs.get('class', '')
            logo_widget.widget.attrs['class'] = (css + ' d-none').strip()


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
        fields = ['dia', 'hora_inicio', 'hora_fin', 'estado', 'estado_otro']
        widgets = {
            'hora_inicio': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
            'hora_fin': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
            'estado': forms.Select(attrs={'class': 'form-select form-select-sm'}),
            'estado_otro': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'maxlength': '30'}),
        }


class CompetidorForm(forms.ModelForm):
    victorias = forms.IntegerField(required=False, min_value=0, label='Victorias')
    derrotas = forms.IntegerField(required=False, min_value=0, label='Derrotas')
    empates = forms.IntegerField(required=False, min_value=0, label='Empates')
    peso_kg = forms.DecimalField(
        required=False, max_digits=5, decimal_places=2, label='Peso (kg)'
    )
    altura_cm = forms.DecimalField(
        required=False, max_digits=5, decimal_places=2, label='Altura (cm)'
    )
    edad = forms.IntegerField(required=False, min_value=0, label='Edad')
    tipo_competidor = forms.ChoiceField(
        choices=[('amateur', 'Amateur'), ('profesional', 'Profesional')],
        widget=forms.RadioSelect,
        required=False,
        label='Tipo'
    )

    class Meta:
        model = models.Competidor
        fields = [
            'avatar',
            'nombre',
            'apellidos',
            'edad',
            'modalidad',
            'peso',
            'peso_kg',
            'altura_cm',
            'sexo',
            'victorias',
            'derrotas',
            'empates',
            'palmares',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            css = field.widget.attrs.get('class', '')
            if not isinstance(field.widget, (forms.CheckboxInput, forms.RadioSelect)):
                field.widget.attrs['class'] = (css + ' form-control').strip()
            if isinstance(field.widget, (
                forms.TextInput,
                forms.EmailInput,
                forms.URLInput,
                forms.NumberInput,
                forms.PasswordInput,
                forms.Textarea,
                forms.DateInput,
                forms.TimeInput,
            )):
                field.widget.attrs.setdefault('placeholder', ' ')

        palmares_field = self.fields.get('palmares')
        if palmares_field:
            palmares_field.widget.attrs['rows'] = 3

        modalidad_field = self.fields.get('modalidad')
        if modalidad_field:
            modalidad_field.choices = [
                ('', '---------'),
                ('schoolboy', 'Schoolboy'),
                ('junior', 'Junior'),
                ('joven', 'Joven'),
                ('elite', 'Elite'),
            ]

        peso_field = self.fields.get('peso')
        if peso_field:
            peso_field.label = 'Categoría'

        tipo_field = self.fields.get('tipo_competidor')
        if tipo_field:
            tipo = 'profesional' if getattr(self.instance, 'modalidad', '') == 'profesional' else 'amateur'
            tipo_field.initial = tipo

        if self.instance and getattr(self.instance, 'record', None):
            try:
                w, l, d = [int(p) for p in self.instance.record.split('-')]
            except Exception:
                w = l = d = 0
            self.fields['victorias'].initial = w
            self.fields['derrotas'].initial = l
            self.fields['empates'].initial = d

        avatar_widget = self.fields.get('avatar')
        if avatar_widget:
            css = avatar_widget.widget.attrs.get('class', '')
            avatar_widget.widget.attrs['class'] = (css + ' d-none').strip()

    def save(self, commit=True):
        wins = self.cleaned_data.get('victorias') or 0
        losses = self.cleaned_data.get('derrotas') or 0
        draws = self.cleaned_data.get('empates') or 0
        self.instance.record = f"{wins}-{losses}-{draws}"

        tipo = self.cleaned_data.get('tipo_competidor')
        if tipo == 'profesional':
            self.instance.modalidad = 'profesional'

        return super().save(commit)


class EntrenadorForm(forms.ModelForm):
    class Meta:
        model = models.Entrenador
        exclude = ['slug', 'club']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            css = field.widget.attrs.get('class', '')
            # Avoid adding form-control to checkbox inputs
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = (css + ' form-control').strip()
            if isinstance(field.widget, (
                forms.TextInput,
                forms.EmailInput,
                forms.URLInput,
                forms.NumberInput,
                forms.PasswordInput,
                forms.Textarea,
                forms.DateInput,
                forms.TimeInput,
            )):
                field.widget.attrs.setdefault('placeholder', ' ')

        # Custom labels with units
        if 'peso' in self.fields:
            self.fields['peso'].label = 'Peso (kg)'
        if 'altura' in self.fields:
            self.fields['altura'].label = 'Altura (cm)'

        avatar_widget = self.fields.get('avatar')
        if avatar_widget:
            css = avatar_widget.widget.attrs.get('class', '')
            avatar_widget.widget.attrs['class'] = (css + ' d-none').strip()


class MiembroForm(forms.ModelForm):
    edad = forms.IntegerField(required=False, min_value=0, label='Edad')
    nacionalidad = forms.ChoiceField(
        choices=[('', 'País')] + COUNTRY_CHOICES,
        required=False,
    )

    class Meta:
        model = models.Miembro
        exclude = ['club']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            css = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = (css + ' form-control').strip()
            if isinstance(field.widget, (
                forms.TextInput,
                forms.EmailInput,
                forms.URLInput,
                forms.NumberInput,
                forms.PasswordInput,
                forms.Textarea,
                forms.DateInput,
                forms.TimeInput,
            )):
                field.widget.attrs.setdefault('placeholder', ' ')

        # Custom placeholders
        if 'peso' in self.fields:
            self.fields['peso'].widget.attrs['placeholder'] = 'peso (kg)'
        if 'altura' in self.fields:
            self.fields['altura'].widget.attrs['placeholder'] = 'altura (cm)'

        avatar_widget = self.fields.get('avatar')
        if avatar_widget:
            css = avatar_widget.widget.attrs.get('class', '')
            avatar_widget.widget.attrs['class'] = (css + ' d-none').strip()

        fecha_widget = self.fields.get('fecha_nacimiento')
        if fecha_widget:
            fecha_widget.widget.input_type = 'date'

        sexo_field = self.fields.get('sexo')
        if sexo_field:
            sexo_field.choices = [('', 'Sexo')] + list(models.Miembro.SEXO_CHOICES)

        nacionalidad_field = self.fields.get('nacionalidad')
        if nacionalidad_field:
            other = [c for c in COUNTRY_CHOICES if c[0] != 'España']
            nacionalidad_field.choices = [('', 'País'), ('España', 'España')] + other
            nacionalidad_field.label = 'País'
            nacionalidad_field.widget.attrs['placeholder'] = 'País'

        # Set default labels for new fields
        if 'localidad' in self.fields:
            self.fields['localidad'].label = 'Localidad'
        if 'codigo_postal' in self.fields:
            self.fields['codigo_postal'].label = 'Código postal'


class PagoForm(forms.ModelForm):
    fecha = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    monto = forms.DecimalField(
        max_digits=8,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'step': '0.01'})
    )

    class Meta:
        model = models.Pago
        fields = ['fecha', 'monto']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['monto'].label = 'Cantidad'
        for name, field in self.fields.items():
            css = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = (css + ' form-control').strip()
            if isinstance(field.widget, (
                forms.TextInput,
                forms.EmailInput,
                forms.URLInput,
                forms.NumberInput,
                forms.PasswordInput,
                forms.Textarea,
                forms.DateInput,
                forms.TimeInput,
            )):
                field.widget.attrs.setdefault('placeholder', ' ')

