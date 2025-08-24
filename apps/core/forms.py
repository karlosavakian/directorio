from django import forms
import re
from apps.core.mixins import UniformFieldsMixin
from apps.clubs.countries import COUNTRY_CHOICES
from apps.clubs.spain import REGION_CHOICES
from django.core.validators import RegexValidator

class TipoUsuarioForm(UniformFieldsMixin, forms.Form):
    tipo = forms.ChoiceField(
        label='Selecciona que eres',
        choices=[
            ('entrenador', 'Entrenador'),
            ('club', 'Club'),
            ('promotor', 'Promotor'),
            ('servicio', 'Servicio'),
        ],
        widget=forms.RadioSelect
    )

class PlanForm(UniformFieldsMixin, forms.Form):
    plan = forms.ChoiceField(
        label='Selecciona el tipo de Plan',
        choices=[
            ('bronce', 'Plan Bronce'),
            ('plata', 'Plan Plata'),
            ('oro', 'Plan Oro'),
        ],
        widget=forms.RadioSelect
    )

class RegistroProfesionalForm(UniformFieldsMixin, forms.Form):
    """Formulario multipaso para seleccionar tipo de usuario y plan."""

    tipo = TipoUsuarioForm.base_fields['tipo']
    plan = PlanForm.base_fields['plan']


class ProRegisterForm(UniformFieldsMixin, forms.Form):
    """Formulario para los datos personales y de dirección del profesional."""

    nombre = forms.CharField(label="Nombre")
    apellidos = forms.CharField(label="Apellidos")
    fecha_nacimiento = forms.DateField(
        label="Fecha de nacimiento",
        widget=forms.DateInput(attrs={"type": "date", "min": "1910-01-01"}),
    )
    dni = forms.CharField(label="DNI/NIE/CIF")
    prefijo = forms.CharField(label="Prefijo")
    telefono = forms.CharField(label="Teléfono")
    sexo = forms.ChoiceField(
        label="Sexo",
        choices=[
            ("", ""),
            ("hombre", "Hombre"),
            ("mujer", "Mujer"),
        ],
    )

    pais = forms.ChoiceField(label="País", choices=COUNTRY_CHOICES)
    comunidad_autonoma = forms.ChoiceField(
        label="Comunidad Autónoma", choices=REGION_CHOICES
    )
    ciudad = forms.CharField(label="Ciudad")
    calle = forms.CharField(label="Calle")
    numero = forms.CharField(label="Número")
    puerta = forms.CharField(label="Puerta", required=False)
    codigo_postal = forms.CharField(label="Código Postal")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.initial.setdefault('pais', 'España')
        country_value = self.data.get('pais') or self.initial.get('pais') or 'España'

        country_field = self.fields.get('pais')
        if country_field:
            country_field.choices = [('', 'País'), ('España', 'España')]
            country_field.initial = country_value

        if country_value == 'España':
            from apps.clubs.spain import REGION_CITIES

            self.fields['ciudad'] = forms.ChoiceField(
                choices=[('', '')], label='Ciudad'
            )

            region_val = self.data.get('comunidad_autonoma') or self.initial.get('comunidad_autonoma', '')
            if region_val:
                self.fields['ciudad'].choices += [
                    (c, c) for c in REGION_CITIES.get(region_val, [])
                ]
        else:
            self.fields['comunidad_autonoma'].widget = forms.HiddenInput()
            self.fields['ciudad'] = forms.ChoiceField(
                choices=[('', '')], label='Ciudad'
            )

        prefijo_field = self.fields.get('prefijo')
        if prefijo_field:
            self.initial.setdefault('prefijo', '+34')
            prefijo_field.widget = forms.HiddenInput(attrs={'class': 'prefijo-input'})

        telefono_field = self.fields.get('telefono')
        if telefono_field:
            css = telefono_field.widget.attrs.get('class', '')
            telefono_field.widget.attrs['class'] = (css + ' phone-input').strip()
            telefono_field.widget.attrs['placeholder'] = 'Telefono'

    def clean_dni(self):
        value = self.cleaned_data.get('dni', '').upper()
        pattern = r'^(?:\d{8}[A-Z]|[XYZ]\d{7}[A-Z]|[A-Z]\d{7}[0-9A-J])$'
        if not re.fullmatch(pattern, value):
            raise forms.ValidationError('Introduce un DNI/NIE/CIF válido.')
        return value

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono', '')
        prefijo = self.cleaned_data.get('prefijo', '')
        digits = re.sub(r'\D', '', telefono)
        if prefijo == '+34':
            if len(digits) > 9:
                raise forms.ValidationError('El teléfono debe tener 9 dígitos.')
            if digits and digits[0] not in '679':
                raise forms.ValidationError('Introduce un número de teléfono válido')
        return digits

    def clean_fecha_nacimiento(self):
        fecha = self.cleaned_data['fecha_nacimiento']
        if fecha and fecha.year < 1910:
            raise forms.ValidationError('La fecha de nacimiento no puede ser anterior a 1910.')
        return fecha


class ProExtraForm(UniformFieldsMixin, forms.Form):
    """Datos adicionales requeridos para completar el perfil profesional."""
    logotipo = forms.ImageField(label="Logotipo")
    username = forms.CharField(
        label="Nombre de usuario",
        min_length=3,
        validators=[RegexValidator(r'^[A-Za-z0-9_-]+$', 'El nombre de usuario solo puede contener letras, números, guiones y guiones bajos.')],
        error_messages={
            "required": "Rellene este campo",
            "min_length": "El nombre de usuario debe tener al menos 3 caracteres",
            "invalid": "El nombre de usuario solo puede contener letras, números, guiones y guiones bajos.",
        },
        widget=forms.TextInput(attrs={"minlength": 3, "placeholder": " ", "pattern": '^[A-Za-z0-9_-]+$'}),
    )
    name = forms.CharField(
        label="Nombre",
        error_messages={"required": "Rellene este campo"},
        widget=forms.TextInput(attrs={"placeholder": " "}),
    )
    about = forms.CharField(label="Bio", widget=forms.Textarea)

