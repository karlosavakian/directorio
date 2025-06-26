# apps/clubs/apps.py

from django.apps import AppConfig

class ClubsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.clubs'  # ✅ Ahora está bien referenciado

    def ready(self):
        # Ensure signals are loaded
        from . import signals  # noqa: F401
