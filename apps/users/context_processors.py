from .forms import LoginForm


def _current_path(request):
    """Return a reasonable URL to redirect to after login."""
    return request.get_full_path()


def login_form(request):
    """Provide a login form instance and next URL for templates."""
    return {
        'login_form': LoginForm(),
        'next_url': _current_path(request),
    }
