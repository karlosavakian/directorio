# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from .models import Profile
from apps.core.mixins import UniformFieldsMixin
import os


def _validate_avatar(avatar):
    """Validate avatar file size and extension."""
    max_size = 2 * 1024 * 1024  # 2MB
    if avatar.size > max_size:
        raise forms.ValidationError(
            'El archivo excede el tamaño máximo de 2MB.'
        )
    ext = os.path.splitext(avatar.name)[1].lower()
    if ext not in ['.jpg', '.jpeg', '.png']:
        raise forms.ValidationError(
            'Formato de imagen no soportado. Usa JPG o PNG.'
        )
    return avatar


class LoginForm(UniformFieldsMixin, AuthenticationForm):
    error_messages = {
        "invalid_login": _("El usuario o la contraseña introducida no es correcta, por favor intente de nuevo"),
        "inactive": _("Esta cuenta está inactiva."),
    }

    username = forms.CharField(
        label="Nombre de usuario",
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
 
class RegistroUsuarioForm(UniformFieldsMixin, UserCreationForm):
    email = forms.EmailField(label='Correo electrónico', required=True, error_messages={"required": "Rellene este campo"})
    username = forms.CharField(
        label='Nombre de usuario',
        min_length=3,
        error_messages={
            'required': 'Rellene este campo',
            'min_length': 'El nombre de usuario debe tener al menos 3 caracteres'
        },
        widget=forms.TextInput(attrs={'minlength': 3})
    )

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
        if password and len(password) < 6:
            raise forms.ValidationError(
                'La contraseña debe tener al menos 6 caracteres.'
            )
        return password

class ProfileForm(UniformFieldsMixin, forms.ModelForm):
    avatar = forms.FileField(required=False)

    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'location']

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if not avatar:
            return avatar
        return _validate_avatar(avatar)


class AccountForm(UniformFieldsMixin, forms.ModelForm):
    avatar = forms.FileField(required=False)
    new_password1 = forms.CharField(
        label='Nueva contraseña', widget=forms.PasswordInput, required=False
    )
    new_password2 = forms.CharField(
        label='Confirmar contraseña', widget=forms.PasswordInput, required=False
    )
    email = forms.EmailField(label='Correo electrónico', required=False)
    username = forms.CharField(
        label='Nombre de usuario',
        min_length=3,
        error_messages={
            'required': 'Rellene este campo',
            'min_length': 'El nombre de usuario debe tener al menos 3 caracteres'
        },
        widget=forms.TextInput(attrs={'minlength': 3})
    )
    notifications = forms.BooleanField(
        label='Recibir notificaciones', required=False
    )

    class Meta:
        model = Profile
        fields = ['avatar', 'notifications']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['username'].initial = user.username
            self.fields['email'].initial = user.email
            self.user = user
        placeholder_fields = ['username', 'email', 'new_password1', 'new_password2']
        for f in placeholder_fields:
            self.fields[f].widget.attrs.setdefault('placeholder', ' ')

         # hide avatar input (preview handled via JS)
        avatar_widget = self.fields['avatar'].widget
        css = avatar_widget.attrs.get('class', '')
        avatar_widget.attrs['class'] = (css + ' d-none').strip()

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if not avatar:
            return avatar
        return _validate_avatar(avatar)

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('new_password1')
        p2 = cleaned.get('new_password2')
        if p1 or p2:
            if p1 != p2:
                self.add_error('new_password2', 'Las contraseñas no coinciden')
            elif p1 and len(p1) < 6:
                self.add_error('new_password1', 'La contraseña es muy corta')
        return cleaned

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = self.user
        user.username = self.cleaned_data['username']
        if self.cleaned_data.get('email'):
            user.email = self.cleaned_data['email']
        new_pass = self.cleaned_data.get('new_password1')
        if new_pass:
            user.set_password(new_pass)
        if commit:
            user.save()
            profile.user = user
            profile.save()
        return profile

