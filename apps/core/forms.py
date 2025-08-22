from django import forms
from apps.core.mixins import UniformFieldsMixin
from apps.clubs.countries import COUNTRY_CHOICES
from apps.clubs.spain import REGION_CHOICES

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
        label="Fecha de nacimiento", widget=forms.DateInput(attrs={"type": "date"})
    )
    dni = forms.CharField(label="DNI/NIE/CIF")
    telefono = forms.CharField(label="Teléfono")
    sexo = forms.ChoiceField(
        label="Sexo",
        choices=[
            ("hombre", "Hombre"),
            ("mujer", "Mujer"),
            ("otro", "Otro"),
        ],
    )

    pais = forms.ChoiceField(label="País", choices=COUNTRY_CHOICES)
    comunidad_autonoma = forms.ChoiceField(
        label="Comunidad Autónoma", choices=REGION_CHOICES
    )
    ciudad = forms.CharField(label="Ciudad")
    calle = forms.CharField(label="Calle")
    numero = forms.CharField(label="Número")
    puerta = forms.CharField(label="Puerta")
    codigo_postal = forms.CharField(label="Código Postal")

