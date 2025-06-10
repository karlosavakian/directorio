# apps/clubs/urls.py

from django.urls import path
from .views import (
    dashboard,
    search,
    public,
    post_create,
    post_update,
    post_delete,
)

urlpatterns = [
    path('resultados/', search.search_results, name='search_results'),
    path('valoraciones/<slug:slug>/', public.ajax_reviews, name='ajax_reviews'),

    path('<slug:slug>/posts/nuevo/', post_create, name='clubpost_create'),
    path('posts/<int:pk>/editar/', post_update, name='clubpost_update'),
    path('posts/<int:pk>/eliminar/', post_delete, name='clubpost_delete'),

    # El perfil público ahora se maneja desde config.urls con la ruta '@slug'

]

