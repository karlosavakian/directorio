# apps/clubs/urls.py

from django.urls import path
from .views import (
    dashboard,
    search,
    public,
    post_create,
    post_update,
    post_delete,
    book_clase,
    cancel_booking,
)

urlpatterns = [
    path('resultados/', search.search_results, name='search_results'),
    path('valoraciones/<slug:slug>/', public.ajax_reviews, name='ajax_reviews'),

    path('<slug:slug>/posts/nuevo/', post_create, name='clubpost_create'),
    path('posts/<int:pk>/editar/', post_update, name='clubpost_update'),
    path('posts/<int:pk>/eliminar/', post_delete, name='clubpost_delete'),

    path('clase/<int:clase_id>/reservar/', book_clase, name='book_clase'),
    path('reserva/<int:pk>/cancelar/', cancel_booking, name='cancel_booking'),

    # El perfil público ahora se maneja desde config.urls con la ruta '@slug'

]

