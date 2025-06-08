# apps/core/templatetags/load_css.py

from django import template
from django.templatetags.static import static
from django.utils.safestring import mark_safe
import os

register = template.Library()
 


@register.simple_tag
def load_css_files():
    """Dynamically loads all CSS files from /static/css/."""
    # ✅ Ruta absoluta al folder de archivos estáticos
    css_folder = os.path.join(os.getcwd(), 'static', 'css')

    try:
        # Listar solo los .css
        files = [f for f in os.listdir(css_folder) if f.endswith('.css')]
    except FileNotFoundError:
        return ""

    # ✅ Generar los tags con el static de Django
    tags = [f'<link rel="stylesheet" href="{static(f"css/{file}")}">' for file in files]

    # Marcar como seguro para HTML
    return mark_safe("\n".join(tags))
