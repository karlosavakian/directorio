# Vistas para búsqueda de clubes, filtros, etc.
# apps/users/views/auth.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.conf import settings
from ..forms import RegistroUsuarioForm, LoginForm
from apps.core.services.email_service import send_welcome_email, send_confirmation_email


def register(request):
    """ Vista para registrar un nuevo usuario """
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            send_welcome_email(user.email)
            send_confirmation_email(user.email)
            # authenticate to attach backend info before login
            auth_user = authenticate(
                request,
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password1"],
            )
            if auth_user is not None:
                login(request, auth_user)
            return redirect('home')
    else:
        form = RegistroUsuarioForm()
    
    return render(request, 'users/register.html', {
        'form': form
    })


class LoginView(DjangoLoginView):
    """Custom login view that handles the remember me option."""
    authentication_form = LoginForm
    template_name = 'users/login.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        remember = form.cleaned_data.get('remember_me')
        if not remember:
            # Expire session when the browser closes
            self.request.session.set_expiry(0)
        else:
            self.request.session.set_expiry(settings.SESSION_COOKIE_AGE)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        next_url = self.request.GET.get(self.redirect_field_name)
        if not next_url:
            ref = self.request.META.get('HTTP_REFERER')
            if ref and ref != self.request.build_absolute_uri():
                next_url = ref
        context['next_url'] = next_url or '/'
        return context
