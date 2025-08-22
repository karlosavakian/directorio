# apps/core/views.py
from django.shortcuts import render, redirect
from ..forms import (
    TipoUsuarioForm,
    PlanForm,
    RegistroProfesionalForm,
    ProRegisterForm,
)
from ..utils.plans import PLANS


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
    """Registro profesional mostrado como formulario multipaso."""
    if not request.user.is_authenticated:
        return redirect('login')

    start_step = 1
    pro_form = ProRegisterForm()

    if request.method == "POST":
        form = RegistroProfesionalForm(request.POST)
        pro_form = ProRegisterForm(request.POST)

        if form.is_valid() and pro_form.is_valid():
            return render(request, "core/registro_pro_success.html")
        start_step = request.POST.get("current_step", 1)
    else:
        form = RegistroProfesionalForm()

    return render(
        request,
        "core/registro_pro.html",
        {
            "form": form,
            "start_step": start_step,
            "pro_form": pro_form,
            "plans": PLANS,
            "current_plan": form["plan"].value(),
        },
    )


def terminos(request):
    """Display terms and conditions page."""
    return render(request, 'core/terminos_condiciones.html')


def privacidad(request):
    """Display privacy policy page."""
    return render(request, 'core/politica_privacidad.html')


def cookies(request):
    """Display cookies policy page."""
    return render(request, 'core/politica_cookies.html')
 
 


