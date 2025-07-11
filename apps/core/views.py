# apps/core/views.py
from django.shortcuts import render


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
 
 
