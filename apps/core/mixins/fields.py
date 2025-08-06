# apps/core/mixins/fields.py
from django import forms

class UniformFieldsMixin:
    """Aplicar estilo uniforme a los campos de un formulario."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css = field.widget.attrs.get('class', '')
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = (css + ' form-check-input').strip()
            else:
                field.widget.attrs['class'] = (css + ' form-control').strip()
            if isinstance(
                field.widget,
                (
                    forms.TextInput,
                    forms.EmailInput,
                    forms.URLInput,
                    forms.NumberInput,
                    forms.PasswordInput,
                    forms.Textarea,
                    forms.DateInput,
                    forms.TimeInput,
                ),
            ):
                field.widget.attrs.setdefault('placeholder', ' ')
