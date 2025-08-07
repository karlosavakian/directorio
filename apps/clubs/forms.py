from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Reseña
from . import models
from django.contrib.auth.forms import AuthenticationForm
from apps.core.mixins import UniformFieldsMixin
from .spain import REGION_CHOICES
from .countries import COUNTRY_CHOICES
import re

class LoginForm(UniformFieldsMixin, AuthenticationForm):
    username = forms.CharField(
        label="Usuario",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label="Contraseña",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

class RegistroUsuarioForm(UniformFieldsMixin, UserCreationForm):
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



class ReseñaForm(UniformFieldsMixin, forms.ModelForm):
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
class ClubPostForm(UniformFieldsMixin, forms.ModelForm):
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

class ClubPostReplyForm(UniformFieldsMixin, forms.ModelForm):
    class Meta:
        model = models.ClubPost
        fields = ['contenido']
        widgets = {
            'contenido': forms.TextInput(attrs={
                'placeholder': 'Escribe una respuesta...',
                'class': 'form-control form-control-sm'
            })
        }


class BookingForm(UniformFieldsMixin, forms.ModelForm):
    class Meta:
        model = models.Booking
        fields = []



class BookingClassForm(UniformFieldsMixin, forms.ModelForm):
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


class ClubForm(UniformFieldsMixin, forms.ModelForm):
    region = forms.ChoiceField(
        choices=[("", "")] + REGION_CHOICES,
        label="Comunidad Autónoma",
        required=False,
    )
    city = forms.CharField(
        label="Ciudad",
        required=False,
    )
    class Meta:
        model = models.Club
        exclude = (
            'created_at',
            'updated_at',
            'verified',
            'owner',
            'category',
            'plan',
            'address',
        )
        labels = {
            'name': 'Nombre del club',
            'slug': 'Usuario',
            'about': 'Bio',
            'country': 'País',
            'region': 'Comunidad Autónoma',
            'city': 'Ciudad',
            'street': 'Calle',
            'number': 'Número',
            'door': 'Puerta',
            'postal_code': 'Código Postal',
            'prefijo': 'Prefijo',
            'phone': 'Teléfono',
            'email': 'Correo electrónico',
            'features': 'Instalaciones y Equipamiento',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure Spain is selected by default
        self.initial.setdefault('country', 'España')
        country_value = (
            self.data.get('country')
            or self.initial.get('country')
            or getattr(getattr(self, 'instance', None), 'country', None)
        )

        country_field = self.fields.get('country')
        if country_field:
            country_field.choices = [('', 'País'), ('España', 'España')]
            country_field.initial = country_value or 'España'

        # Set initial values from stored names
        if self.instance.pk:
            if self.instance.region:
                self.fields['region'].initial = self.instance.region
            if self.instance.city:
                self.fields['city'].initial = self.instance.city

        # Dynamic location fields based on country selection
        if country_value == 'España':
            from .spain import REGION_CITIES

            # Convert city to a choice field for Spanish clubs
            self.fields['city'] = forms.ChoiceField(
                choices=[("", "")], label="Ciudad", required=False
            )

            region_val = self.data.get('region') or self.initial.get('region') or getattr(self.instance, 'region', '')
            if region_val:
                self.fields['city'].choices += [
                    (c, c) for c in REGION_CITIES.get(region_val, [])
                ]
            if self.instance.city:
                self.fields['city'].initial = self.instance.city
        else:
            # Hide region field for non-Spanish countries and prepare city choices
            self.fields['region'].widget = forms.HiddenInput()
            self.fields['city'] = forms.ChoiceField(
                choices=[("", "")], label="Ciudad", required=False
            )
            if self.instance.city:
                self.fields['city'].choices += [(self.instance.city, self.instance.city)]
                self.fields['city'].initial = self.instance.city

        for name, field in self.fields.items():
            css = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = (css + ' form-control').strip()
            if isinstance(
                field.widget,
                (forms.TextInput, forms.EmailInput,
                 forms.URLInput, forms.NumberInput,
                 forms.PasswordInput, forms.Textarea,
                 forms.DateInput, forms.TimeInput, forms.Select),
            ):
                field.widget.attrs.setdefault('placeholder', ' ')
            if name == 'slug':
                field.widget.attrs['data-current'] = getattr(self.instance, 'slug', '')
                field.widget.attrs['minlength'] = 3
                field.required = True

        prefijo_field = self.fields.get('prefijo')
        if prefijo_field:
            self.initial.setdefault('prefijo', '+34')
            prefijo_field.widget = forms.HiddenInput(attrs={'class': 'prefijo-input'})

        telefono_field = self.fields.get('telefono')
        if telefono_field:
            css = telefono_field.widget.attrs.get('class', '')
            telefono_field.widget.attrs['class'] = (css + ' phone-input').strip()
            telefono_field.widget.attrs['placeholder'] = ' '

        phone_field = self.fields.get('phone')
        if phone_field:
            css = phone_field.widget.attrs.get('class', '')
            phone_field.widget.attrs['class'] = (css + ' phone-input').strip()
            phone_field.widget.attrs['placeholder'] = ' '

        logo_widget = self.fields.get('logo')
        if logo_widget:
            css = logo_widget.widget.attrs.get('class', '')
            logo_widget.widget.attrs['class'] = (css + ' d-none').strip()

    def clean_slug(self):
        slug = self.cleaned_data.get('slug', '').lstrip('@')
        if len(slug) < 3:
            raise forms.ValidationError('Introduce un nombre con al menos 3 carácteres')
        if models.Club.objects.exclude(pk=self.instance.pk).filter(slug=slug).exists():
            raise forms.ValidationError('Este usuario ya está en uso.')
        return slug

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '')
        prefijo = self.cleaned_data.get('prefijo', '')
        digits = re.sub(r'\D', '', phone)
        if prefijo == '+34' and len(digits) > 9:
            raise forms.ValidationError('El teléfono debe tener 9 dígitos.')
        return digits

    def save(self, commit=True):
        instance = super().save(commit=False)
        region = self.cleaned_data.get('region')
        city = self.cleaned_data.get('city')
        if region:
            instance.region = region
        if city:
            instance.city = city
        if commit:
            instance.save()
            self.save_m2m()
        return instance


class CancelBookingForm(UniformFieldsMixin, forms.Form):
    """Simple form used to confirm cancellation."""
    pass


class ClubPhotoForm(UniformFieldsMixin, forms.ModelForm):
    class Meta:
        model = models.ClubPhoto
        fields = ['image']


class HorarioForm(UniformFieldsMixin, forms.ModelForm):
    class Meta:
        model = models.Horario
        fields = ['dia', 'hora_inicio', 'hora_fin', 'estado', 'estado_otro']
        widgets = {
            'hora_inicio': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
            'hora_fin': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
            'estado': forms.Select(attrs={'class': 'form-select form-select-sm'}),
            'estado_otro': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'maxlength': '30'}),
        }


class CompetidorForm(UniformFieldsMixin, forms.ModelForm):
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


class EntrenadorForm(UniformFieldsMixin, forms.ModelForm):
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


class MiembroForm(UniformFieldsMixin, forms.ModelForm):
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

        prefijo_field = self.fields.get('prefijo')
        if prefijo_field:
            self.initial.setdefault('prefijo', '+34')
            prefijo_field.widget = forms.HiddenInput(attrs={'class': 'prefijo-input'})

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
            nacionalidad_field.choices = [('', 'País'), ('España', 'España')]
            nacionalidad_field.label = 'País'
            nacionalidad_field.widget.attrs['placeholder'] = 'País'
            nacionalidad_field.initial = 'España'

        # Set default labels for new fields
        if 'localidad' in self.fields:
            self.fields['localidad'].label = 'Localidad'
        if 'codigo_postal' in self.fields:
            self.fields['codigo_postal'].label = 'Código postal'

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono', '')
        prefijo = self.cleaned_data.get('prefijo', '')
        digits = re.sub(r'\D', '', telefono)
        if prefijo == '+34' and len(digits) > 9:
            raise forms.ValidationError('El teléfono debe tener 9 dígitos.')
        return digits


class PagoForm(UniformFieldsMixin, forms.ModelForm):
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


class ClubMessageForm(UniformFieldsMixin, forms.ModelForm):
    class Meta:
        model = models.ClubMessage
        fields = ['content']
        widgets = {
            'content': forms.Textarea(
                attrs={
                    'class': 'form-control form-control-sm w-100',
                    'rows': 1,
                    'style': 'height:30px; max-height:30px;',
                    'placeholder': 'Mensaje...'
                }
            )
        }
