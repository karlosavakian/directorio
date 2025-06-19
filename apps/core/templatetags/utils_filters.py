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
