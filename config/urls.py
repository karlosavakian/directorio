# directorio_boxeo/config/urls.py

from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from apps.clubs.views import public as club_public
from apps.clubs.views import messages as club_messages
from apps.clubs.views.dashboard import dashboard
from apps.users.views import profile as user_profile
  
from apps.users.forms import LoginForm
from apps.core.views.public import error_404

urlpatterns = [
    path('django-admin/', admin.site.urls),

    # Core: Página principal
    path('', include('apps.core.urls')),

    # Perfil público de clubs
    path('admin/', dashboard, name='club_dashboard'),
    path('@<slug:slug>/inscribirse/', club_public.member_signup, name='club_member_signup'),
    path('@<slug:slug>/reservar/', club_public.booking_form, name='club_booking'),
    path('@<slug:slug>/', club_public.club_profile, name='club_profile'),
    path('coach/@<slug:slug>/', club_public.coach_profile, name='coach_profile'),

    # Perfil público de usuarios
    path('profile/<str:username>/', user_profile.profile_detail, name='user_profile'),

    # Bandeja y conversaciones de mensajes
    path('mensajes/', club_messages.conversation, name='conversation'),
    path('mensajes/chat/<str:chat_id>/', club_messages.conversation, name='chat'),
    path('mensaje/<int:pk>/like/', club_messages.message_toggle_like, name='message_like'),

    # Clubs: Gestión de Clubs y búsqueda
    path('clubs/', include('apps.clubs.urls')),

    # Blog posts
    path('blog/', include('apps.blog.urls')),


    # Rutas de autenticación sin el prefijo "accounts/"
    path('', include('apps.users.urls')),
    path('', include('allauth.urls')),
]

# Custom error handlers
handler404 = "apps.core.views.public.error_404"

# Archivos estáticos en modo DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Catch-all pattern for unmatched URLs
urlpatterns += [re_path(r"^.*$", error_404)]
