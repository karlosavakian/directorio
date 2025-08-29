# apps/core/stripe_client.py
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
import stripe, logging

log = logging.getLogger(__name__)

def get_stripe() -> stripe:
    key = getattr(settings, "STRIPE_SECRET_KEY", "") or ""
    if not key:
        raise ImproperlyConfigured("STRIPE_SECRET_KEY vacío")
    if key.startswith("pk_"):
        # Evita que nunca más se cuele una pk en backend
        masked = key[:7] + "…" + key[-4:]
        log.error("Clave Stripe inválida en backend (parece publishable): %s", masked)
        raise ImproperlyConfigured("Se está usando una publishable key (pk_...) en backend")
    stripe.api_key = key
    # Opcional, identifica tu app ante Stripe
    stripe.set_app_info(name="clubsdeboxeo", version="1.0.0")
    return stripe
