from django import template

register = template.Library()

@register.filter
def initials(value):
    """Return initials from a full name string."""
    if not value:
        return ""
    parts = [p for p in str(value).split() if p]
    if not parts:
        return ""
    initials = "".join(p[0] for p in parts[:2])
    return initials.upper()


@register.filter
def get_item(dictionary, key):
    """Return dictionary value for the given key."""
    if isinstance(dictionary, dict):
        return dictionary.get(key, '')
    return ''


@register.filter
def time_since_short(value):
    """Return relative time from ``value`` to now in Spanish."""
    if not value:
        return ""
    from django.utils import timezone

    now = timezone.now()
    diff = now - value
    seconds = int(diff.total_seconds())

    if seconds < 60:
        return f"hace {seconds} segundos"
    minutes = seconds // 60
    if minutes < 60:
        return f"hace {minutes} minutos"
    hours = minutes // 60
    if hours < 24:
        return f"hace {hours}h"
    days = hours // 24
    if days < 7:
        return f"hace {days}d"
    weeks = days // 7
    if weeks == 1:
        return "hace 1 semana"
    return f"hace {weeks} semanas"
