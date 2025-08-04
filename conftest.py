import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from django.conf import settings
settings.ALLOWED_HOSTS.append('testserver')
