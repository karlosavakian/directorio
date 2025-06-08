# apps/clubs/urls.py

from django.urls import path
from .views import (
    dashboard,
    search,
    public,
)

urlpatterns = [
    path('resultados/', search.search_results, name='search_results'),
    path('valoraciones/<slug:slug>/', public.ajax_reviews, name='ajax_reviews'),
    
    # El perfil público ahora se maneja desde config.urls con la ruta '@slug'
 
]

