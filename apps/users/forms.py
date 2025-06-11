# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from .models import Profile


class LoginForm(AuthenticationForm):
    error_messages = {
        "invalid_login": _("El usuario o la contraseña introducida no es correcta, por favor intente de nuevo"),
        "inactive": _("Esta cuenta está inactiva."),
    }

    username = forms.CharField(
        label="Usuario",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        error_messages={"required": "Rellene este campo"},
    )
    password = forms.CharField(
        label="Contraseña",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        error_messages={"required": "Rellene este campo"},
    )
    remember_me = forms.BooleanField(
        label="Recordarme",
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mark "recordar contraseña" checked by default
        self.fields["remember_me"].initial = True
 
class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField(label='Correo electrónico', required=True, error_messages={"required": "Rellene este campo"})

    error_messages = {
        **UserCreationForm.error_messages,
        'password_mismatch': _('Las contraseñas no coinciden'),
    }

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
        # Custom required messages
        for field in ['username', 'password1', 'password2', 'email']:
            self.fields[field].error_messages['required'] = 'Rellene este campo'

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este correo electrónico ya está registrado')
        return email

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if password:
            if len(password) < 6 or not any(c.islower() for c in password) or not any(c.isupper() for c in password) or not any(c.isdigit() for c in password):
                raise forms.ValidationError(
                    'La contraseña debe tener al menos 6 caracteres e incluir mayúsculas, minúsculas y números.'
                )
        return password

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'location']

