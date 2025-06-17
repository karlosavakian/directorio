# apps/clubs/urls.py

from django.urls import path
from .views import (
    search,
    public,
    post_create,
    post_update,
    post_delete,
    book_clase,
    cancel_booking,
)
from apps.clubs.views.dashboard import (
    dashboard,
    club_edit,
    clase_create,
    clase_update,
    clase_delete,
)

urlpatterns = [
    path('resultados/', search.search_results, name='search_results'),
    path('valoraciones/<slug:slug>/', public.ajax_reviews, name='ajax_reviews'),

    path('<slug:slug>/dashboard/', dashboard, name='club_dashboard'),
    path('<slug:slug>/editar/', club_edit, name='club_edit'),
    path('<slug:slug>/clase/nueva/', clase_create, name='clase_create'),
    path('clase/<int:pk>/editar/', clase_update, name='clase_update'),
    path('clase/<int:pk>/eliminar/', clase_delete, name='clase_delete'),

    path('<slug:slug>/posts/nuevo/', post_create, name='clubpost_create'),
    path('posts/<int:pk>/editar/', post_update, name='clubpost_update'),
    path('posts/<int:pk>/eliminar/', post_delete, name='clubpost_delete'),

    path('clase/<int:clase_id>/reservar/', book_clase, name='book_clase'),
    path('reserva/<int:pk>/cancelar/', cancel_booking, name='cancel_booking'),

    # El perfil público ahora se maneja desde config.urls con la ruta '@slug'

]

