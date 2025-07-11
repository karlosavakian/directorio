from django import forms

class ProfessionalRegistrationForm(forms.Form):
    REGISTRATION_CHOICES = [
        ('entrenador', 'Alta entrenador'),
        ('club', 'Alta club'),
        ('manager', 'Alta manager'),
        ('servicio', 'Alta servicio'),
    ]
    PLAN_CHOICES = [
        ('gratis', 'Plan Gratuito'),
        ('amateur', 'Plan Amateur'),
        ('pro', 'Plan Pro'),
    ]

    registration_type = forms.ChoiceField(
        label='Tipo de alta',
        choices=REGISTRATION_CHOICES,
        widget=forms.RadioSelect
    )
    plan = forms.ChoiceField(
        label='Plan de suscripción',
        choices=PLAN_CHOICES,
        widget=forms.RadioSelect
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = (css + ' form-check-input').strip()
