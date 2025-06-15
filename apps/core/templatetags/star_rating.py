from django import template
from django.utils.safestring import mark_safe

register = template.Library()

STAR_PATH = 'M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z'

@register.simple_tag
def render_stars(rating):
    """Return SVG star icons representing the given rating."""
    try:
        rating = float(rating)
    except (TypeError, ValueError):
        rating = 0
    filled = int(round(rating))
    filled = max(0, min(filled, 5))
    empty = 5 - filled
    def star(color):
        return f'<svg width="20" height="20" viewBox="0 0 24 24" fill="{color}" stroke="#666"><path d="{STAR_PATH}"/></svg>'
    stars_html = ''.join(star('#000') for _ in range(filled))
    stars_html += ''.join(star('transparent') for _ in range(empty))
    return mark_safe(stars_html)
