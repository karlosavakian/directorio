from django import forms

class TipoUsuarioForm(forms.Form):
    tipo = forms.ChoiceField(
        label='Selecciona que eres',
        choices=[
            ('entrenador', 'Entrenador'),
            ('club', 'Club'),
            ('manager', 'Manager'),
            ('servicio', 'Servicio'),
        ],
        widget=forms.RadioSelect
    )

class PlanForm(forms.Form):
    plan = forms.ChoiceField(
        label='Selecciona el tipo de Plan',
        choices=[
            ('gratis', 'Plan Gratuito'),
            ('amateur', 'Plan Amateur'),
            ('pro', 'Plan Pro'),
        ],
        widget=forms.RadioSelect
    )

class BaseInfoForm(forms.Form):
    nombre = forms.CharField(label='Nombre', max_length=100)
    email = forms.EmailField(label='Correo')
    telefono = forms.CharField(label='Teléfono', required=False)
    descripcion = forms.CharField(label='Descripción', widget=forms.Textarea, required=False)


class RegistroProForm(forms.Form):
    """Formulario combinado para el registro profesional."""
    tipo = TipoUsuarioForm.base_fields['tipo']
    plan = PlanForm.base_fields['plan']
    nombre = BaseInfoForm.base_fields['nombre']
    email = BaseInfoForm.base_fields['email']
    telefono = BaseInfoForm.base_fields['telefono']
    descripcion = BaseInfoForm.base_fields['descripcion']

