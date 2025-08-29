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
    CoachFormSet,
)
from ..utils.plans import PLANS
from apps.clubs.models import Club, Entrenador


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
    coach_formset = CoachFormSet(prefix="coaches")

    if request.method == "POST":
        form = RegistroProfesionalForm(request.POST)
        pro_form = ProRegisterForm(request.POST)
        extra_form = ProExtraForm(request.POST, request.FILES)
        coach_formset = CoachFormSet(request.POST, prefix="coaches")
        if form.is_valid() and pro_form.is_valid() and extra_form.is_valid():
            coach_valid = True
            if form.cleaned_data["tipo"] == "club":
                coach_valid = coach_formset.is_valid()
            if coach_valid:
                user = request.user
                profile = user.profile
                profile.plan = form.cleaned_data["plan"]
                profile.save()

                user.username = extra_form.cleaned_data["username"]
                user.first_name = pro_form.cleaned_data["nombre"]
                user.last_name = pro_form.cleaned_data["apellidos"]
                user.save()

                if form.cleaned_data["tipo"] == "entrenador":
                    club = Club.objects.create(
                        owner=user,
                        name=extra_form.cleaned_data["name"],
                        about=extra_form.cleaned_data["about"],
                        logo=extra_form.cleaned_data.get("logotipo"),
                        profilepic=extra_form.cleaned_data.get("logotipo"),
                        prefijo=pro_form.cleaned_data.get("prefijo", ""),
                        phone=pro_form.cleaned_data.get("telefono", ""),
                        email=user.email,
                        country=pro_form.cleaned_data.get("pais", ""),
                        region=pro_form.cleaned_data.get("comunidad_autonoma", ""),
                        city=pro_form.cleaned_data.get("ciudad", ""),
                        street=pro_form.cleaned_data.get("calle", ""),
                        number=pro_form.cleaned_data.get("numero"),
                        door=pro_form.cleaned_data.get("puerta", ""),
                        postal_code=pro_form.cleaned_data.get("codigo_postal", ""),
                        category="entrenador",
                        plan=form.cleaned_data["plan"],
                    )
                    club.features.set(extra_form.cleaned_data["features"])
                    club.coach_features.set(extra_form.cleaned_data["coach_features"])
                elif form.cleaned_data["tipo"] == "club":
                    club = Club.objects.create(
                        owner=user,
                        name=extra_form.cleaned_data["name"],
                        about=extra_form.cleaned_data["about"],
                        logo=extra_form.cleaned_data.get("logotipo"),
                        profilepic=extra_form.cleaned_data.get("logotipo"),
                        prefijo=pro_form.cleaned_data.get("prefijo", ""),
                        phone=pro_form.cleaned_data.get("telefono", ""),
                        email=user.email,
                        country=pro_form.cleaned_data.get("pais", ""),
                        region=pro_form.cleaned_data.get("comunidad_autonoma", ""),
                        city=pro_form.cleaned_data.get("ciudad", ""),
                        street=pro_form.cleaned_data.get("calle", ""),
                        number=pro_form.cleaned_data.get("numero"),
                        door=pro_form.cleaned_data.get("puerta", ""),
                        postal_code=pro_form.cleaned_data.get("codigo_postal", ""),
                        category="club",
                        plan=form.cleaned_data["plan"],
                    )
                    club.features.set(extra_form.cleaned_data["features"])
                    club.coach_features.set(extra_form.cleaned_data["coach_features"])
                    for coach_data in coach_formset.cleaned_data:
                        if coach_data:
                            Entrenador.objects.create(
                                club=club,
                                nombre=coach_data["nombre"],
                                apellidos=coach_data["apellidos"],
                            )
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
            "coach_formset": coach_formset,
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


@csrf_exempt
@require_POST
def create_payment_intent(request):
    """Create a Stripe PaymentIntent in test mode."""
    stripe.api_key = settings.STRIPE_SECRET_KEY
    intent = stripe.PaymentIntent.create(
        amount=1000,
        currency="usd",
    )
    return JsonResponse({"clientSecret": intent.client_secret})


def checkout_success(request):
    """Display Stripe checkout success page."""
    return render(request, "core/checkout_success.html")


def checkout_cancel(request):
    """Display Stripe checkout cancel page."""
    return render(request, "core/checkout_cancel.html")


def error_404(request, exception=None):
    """Display custom 404 page."""
    return render(request, '404.html', status=404)
