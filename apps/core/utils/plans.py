"""Utility definitions for subscription plans used across the site."""

# Centralized list of available plans so templates can render
# consistent information whether they are used on the profile or
# professional registration pages.

PLANS = [
    {
        "value": "bronce",
        "title": "Plan Bronce",
        "price": "0€ / mes",
        "features": [
            "Presencia básica en el directorio",
            "Publicación de eventos",
            "Acceso a valoraciones",
        ],
    },
    {
        "value": "plata",
        "title": "Plan Plata",
        "price": "9€ / mes",
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
        "price": "19€ / mes",
        "features": [
            "Todos los beneficios del Plan Plata",
            "Badge de verificación",
            "Herramientas de marketing avanzadas",
        ],
    },
]

