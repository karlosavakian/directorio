# apps/core/views.py
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth.decorators import login_required

import stripe
from ..forms import (
    TipoUsuarioForm,
    PlanForm,
    RegistroProfesionalForm,
    ProRegisterForm,
    ProExtraForm,
    CoachFormSet,
)
from ..utils.plans import PLANS, PLAN_PRICES
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
                payment_valid = True
                plan = form.cleaned_data["plan"]
                if plan in ["plata", "oro"]:
                    amount_lookup = {"plata": 900, "oro": 1900}
                    payment_intent_id = request.POST.get("payment_intent_id")
                    stripe.api_key = settings.STRIPE_SECRET_KEY
                    try:
                        intent = stripe.PaymentIntent.retrieve(payment_intent_id)
                        expected_amount = amount_lookup.get(plan)
                        if intent.status != "succeeded" or intent.amount_received != expected_amount:
                            payment_valid = False
                    except Exception:
                        payment_valid = False
                if payment_valid:
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
                else:
                    form.add_error(None, "Error al verificar el pago.")
                    messages.error(request, "Hubo un problema con el pago. Inténtalo de nuevo.")
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
 
@login_required
@require_POST
def create_payment_intent(request):
    """Create a Stripe PaymentIntent for the selected plan."""
    plan = request.POST.get("plan")
    amount = PLAN_PRICES.get(plan)
    if not amount:
        return JsonResponse({"error": "Invalid plan"}, status=400)

    stripe.api_key = settings.STRIPE_SECRET_KEY
    try:
        intent = stripe.PaymentIntent.create(amount=amount, currency="eur")
    except stripe.error.StripeError as e:
        return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"clientSecret": intent.client_secret})


@login_required
@require_POST
def create_checkout_session(request):
    """Create a Stripe Checkout Session for the selected plan."""
    plan = request.POST.get("plan")
    amount = PLAN_PRICES.get(plan)
    if not amount:
        return JsonResponse({"error": "Invalid plan"}, status=400)

    stripe.api_key = settings.STRIPE_SECRET_KEY
    try:
        session = stripe.checkout.Session.create(
            mode="payment",
            line_items=[
                {
                    "price_data": {
                        "currency": "eur",
                        "product_data": {"name": plan},
                        "unit_amount": amount,
                    },
                    "quantity": 1,
                }
            ],
            success_url=request.build_absolute_uri("/"),
            cancel_url=request.build_absolute_uri("/"),
        )
    except stripe.error.StripeError as e:
        return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"id": session.id})


def error_404(request, exception=None):
    """Display custom 404 page."""
    return render(request, '404.html', status=404)
