# apps/core/views.py
from django.shortcuts import render, redirect
from ..forms import RegistroProForm


def home(request):
    search_query = request.GET.get('q', '').strip()
    return render(request, 'core/home.html', {
        'search_query': search_query,
    })


def ayuda(request): 
    return render(request, 'core/ayuda.html')

def pro(request):
    return render(request, 'core/pro.html')


def registro_profesional(request):
    """Registro profesional en un único formulario controlado por JavaScript."""
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        form = RegistroProForm(request.POST)
        if form.is_valid():
            return render(request, 'core/registro_pro_success.html')
    else:
        form = RegistroProForm()

    return render(request, 'core/registro_pro.html', {'form': form})


def terminos(request):
    """Display terms and conditions page."""
    return render(request, 'core/terminos_condiciones.html')


def privacidad(request):
    """Display privacy policy page."""
    return render(request, 'core/politica_privacidad.html')


def cookies(request):
    """Display cookies policy page."""
    return render(request, 'core/politica_cookies.html')
 
 


