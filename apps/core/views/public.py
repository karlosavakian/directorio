# apps/core/views.py
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

import stripe
from ..forms import (
    TipoUsuarioForm,
    PlanForm,
    RegistroProfesionalForm,
    ProRegisterForm,
    ProExtraForm,
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
    extra_form = ProExtraForm(
        initial={
            "username": request.user.username,
            "name": request.user.get_full_name(),
        }
    )

    if request.method == "POST":
        form = RegistroProfesionalForm(request.POST)
        pro_form = ProRegisterForm(request.POST)
        extra_form = ProExtraForm(request.POST, request.FILES)

        if form.is_valid() and pro_form.is_valid() and extra_form.is_valid():
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
            "extra_form": extra_form,
            "plans": PLANS,
            "current_plan": form["plan"].value(),
            "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
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
 
 

@csrf_exempt
@require_POST
def create_checkout_session(request):
    """Create a Stripe Checkout session in test mode."""
    stripe.api_key = settings.STRIPE_SECRET_KEY
    session = stripe.checkout.Session.create(
        mode="payment",
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {"name": "Test plan"},
                    "unit_amount": 1000,
                },
                "quantity": 1,
            }
        ],
        success_url=request.build_absolute_uri(reverse("checkout_success")),
        cancel_url=request.build_absolute_uri(reverse("checkout_cancel")),
    )
    return JsonResponse({"sessionId": session.id})


def checkout_success(request):
    """Display Stripe checkout success page."""
    return render(request, "core/checkout_success.html")


def checkout_cancel(request):
    """Display Stripe checkout cancel page."""
    return render(request, "core/checkout_cancel.html")


def error_404(request, exception=None):
    """Display custom 404 page."""
    return render(request, '404.html', status=404)
