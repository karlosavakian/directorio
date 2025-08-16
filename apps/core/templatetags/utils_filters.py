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


@register.filter(is_safe=True)
def youtube_embed(text):
    """Replace YouTube links in ``text`` with embed iframe."""
    if not text:
        return ""
    import re
    from django.utils.html import escape
    from django.utils.safestring import mark_safe

    pattern = (
        r"(https?://(?:www\.)?"
        r"(?:youtube\.com/(?:watch\?v=|shorts/)|youtu\.be/)([\w-]+))"
        r"(?:\S*)"
    )
    match = re.search(pattern, text)
    if not match:
        return escape(text)

    video_id = match.group(2)
    cleaned = re.sub(pattern, "", text).strip()
    embed = (
        f'<iframe width="560" height="315" '
        f'src="https://www.youtube.com/embed/{video_id}" '
        f'frameborder="0" allowfullscreen></iframe>'
    )
    safe_text = escape(cleaned)
    html = f"<p>{safe_text}</p>" if cleaned else ""
    html += embed
    return mark_safe(html)


@register.filter
def safe_url(file_field):
    """Return the file URL with a cache-busting timestamp if available."""
    try:
        if not file_field:
            return ""
        url = file_field.url
        try:
            modified = file_field.storage.get_modified_time(file_field.name)
        except Exception:
            modified = None
        if modified:
            from django.utils import timezone
            if timezone.is_aware(modified):
                modified = timezone.make_naive(modified, timezone.utc)
            url = f"{url}?v={int(modified.timestamp())}"
        return url
    except (ValueError, AttributeError):
        return ""


@register.filter
def get_list(querydict, key):
    """Return list of values for ``key`` in a ``QueryDict``."""
    try:
        return querydict.getlist(key)
    except AttributeError:
        return []


@register.filter
def message_timestamp(value):
    """Return only the time portion of ``value`` in 24h format."""
    if not value:
        return ""

    from django.utils import timezone

    value = timezone.localtime(value)
    return value.strftime("%H:%M")


@register.filter
def message_day(value):
    """Return 'Hoy', 'Ayer' or formatted date for ``value``."""
    if not value:
        return ""

    from datetime import timedelta
    from django.utils import timezone

    value_date = timezone.localtime(value).date()
    today = timezone.localtime(timezone.now()).date()

    if value_date == today:
        return "Hoy"
    if value_date == today - timedelta(days=1):
        return "Ayer"

    return value_date.strftime("%d/%m/%Y")
