# directorio_boxeo/config/urls.py

from django.contrib import admin
from django.urls import path, include    
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
  
from apps.users.forms import LoginForm   
 
urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Core: Página principal
    path('', include('apps.core.urls')),  

    # Clubs: Gestión de Clubs y búsqueda
    path('clubs/', include('apps.clubs.urls')),


    path('accounts/', include('apps.users.urls')),  # <-- Aquí incluimos las rutas de registro
]

# Archivos estáticos en modo DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)