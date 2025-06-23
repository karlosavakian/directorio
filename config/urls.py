# directorio_boxeo/config/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from apps.clubs.views import public as club_public
from apps.clubs.views.dashboard import dashboard
from apps.users.views import profile as user_profile
  
from apps.users.forms import LoginForm   
 
urlpatterns = [
    path('admin/', admin.site.urls),

    # Core: Página principal
    path('', include('apps.core.urls')),

    # Perfil público de clubs
    path('@<slug:slug>/admin/', dashboard, name='club_dashboard'),
    path('@<slug:slug>/feed/', club_public.club_feed, name='club_feed'),
    path('@<slug:slug>/', club_public.club_profile, name='club_profile'),
    path('coach/@<slug:slug>/', club_public.coach_profile, name='coach_profile'),

    # Perfil público de usuarios
    path('profile/<str:username>/', user_profile.profile_detail, name='user_profile'),

    # Clubs: Gestión de Clubs y búsqueda
    path('clubs/', include('apps.clubs.urls')),


    # Rutas de autenticación sin el prefijo "accounts/"
    path('', include('apps.users.urls')),
    path('', include('allauth.urls')),
]

# Archivos estáticos en modo DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
