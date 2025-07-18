from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.users'

    def ready(self):
        # Import signal handlers to ensure profiles are created when users are added
        from . import signals  # noqa: F401
