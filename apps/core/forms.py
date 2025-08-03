from django import forms

class TipoUsuarioForm(forms.Form):
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

class PlanForm(forms.Form):
    plan = forms.ChoiceField(
        label='Selecciona el tipo de Plan',
        choices=[
            ('bronce', 'Plan Bronce'),
            ('plata', 'Plan Plata'),
            ('oro', 'Plan Oro'),
        ],
        widget=forms.RadioSelect
    )

class RegistroProfesionalForm(forms.Form):
    """Formulario multipaso para seleccionar tipo de usuario y plan."""

    tipo = TipoUsuarioForm.base_fields['tipo']
    plan = PlanForm.base_fields['plan']

