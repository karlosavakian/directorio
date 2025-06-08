# apps/clubs/urls.py

from django.urls import path
from .views import (
    dashboard, 
    search,
    public, 
)

urlpatterns = [
    path('resultados/', search.search_results, name='search_results'),
    
    # El perfil público ahora se maneja desde config.urls con la ruta '@slug'
 
]

