from .forms import LoginForm


def login_form(request):
    """Provide a login form instance for use in templates."""
    return {'login_form': LoginForm()}
