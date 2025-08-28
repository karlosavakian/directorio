"""Utility definitions for subscription plans used across the site."""

# Centralized price definitions (amounts in euro cents) so both the
# templates and Stripe interactions stay in sync.
PLAN_PRICES = {
    "bronce": 0,
    "plata": 900,
    "oro": 1900,
}

# Centralized list of available plans so templates can render
# consistent information whether they are used on the profile or
# professional registration pages.
PLANS = [
    {
        "value": "bronce",
        "title": "Plan Bronce",
        "features": [
            "Presencia básica en el directorio",
            "Publicación de eventos",
            "Acceso a valoraciones",
        ],
    },
    {
        "value": "plata",
        "title": "Plan Plata",
        "features": [
            "Todos los beneficios del Plan Bronce",
            "Publicaciones ilimitadas",
            "Estadísticas básicas",
        ],
        "featured": True,
    },
    {
        "value": "oro",
        "title": "Plan Oro",
        "features": [
            "Todos los beneficios del Plan Plata",
            "Badge de verificación",
            "Herramientas de marketing avanzadas",
        ],
    },
]

# Enrich plan definitions with price information derived from PLAN_PRICES
for plan in PLANS:
    amount = PLAN_PRICES[plan["value"]]
    plan["amount"] = amount
    plan["price"] = f"{amount // 100}€ / mes"
