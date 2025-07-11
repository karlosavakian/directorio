# apps/core/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import ProfessionalRegistrationForm


def home(request):
    search_query = request.GET.get('q', '').strip()
    return render(request, 'core/home.html', {
        'search_query': search_query,
    })


def ayuda(request):
    """Display frequently asked questions."""
    return render(request, 'core/ayuda.html')


def planes(request):
    """Display available subscription plans."""
    return render(request, 'core/planes.html')


def terminos(request):
    """Display terms and conditions page."""
    return render(request, 'core/terminos_condiciones.html')


def privacidad(request):
    """Display privacy policy page."""
    return render(request, 'core/politica_privacidad.html')


def cookies(request):
    """Display cookies policy page."""
    return render(request, 'core/politica_cookies.html')


@login_required
def professional_register(request):
    """Handle professional registration form."""
    if request.method == 'POST':
        form = ProfessionalRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Solicitud enviada correctamente.')
            return redirect('planes')
    else:
        form = ProfessionalRegistrationForm()
    return render(request, 'core/professional_register.html', {
        'form': form,
    })
 
 
