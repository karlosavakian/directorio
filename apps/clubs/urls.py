# apps/clubs/urls.py

from django.urls import path
from apps.clubs.views import (
    search,
    public,
    post_create,
    post_update,
    post_delete,
    post_reply,
    post_toggle_like,
    cancel_booking,
)
from apps.clubs.views.dashboard import (
    dashboard,
    club_edit,
    photo_upload,
    photo_delete,
    competidor_create,
    competidor_update,
    competidor_delete,
    entrenador_create,
    entrenador_update,
    entrenador_delete,
)

urlpatterns = [
    path('resultados/', search.search_results, name='search_results'),
    path('valoraciones/<slug:slug>/', public.ajax_reviews, name='ajax_reviews'),

    path('<slug:slug>/editar/', club_edit, name='club_edit'),

    path('<slug:slug>/foto/nueva/', photo_upload, name='clubphoto_upload'),
    path('foto/<int:pk>/eliminar/', photo_delete, name='clubphoto_delete'),


    path('<slug:slug>/competidor/nuevo/', competidor_create, name='competidor_create'),
    path('competidor/<int:pk>/editar/', competidor_update, name='competidor_update'),
    path('competidor/<int:pk>/eliminar/', competidor_delete, name='competidor_delete'),

    path('<slug:slug>/entrenador/nuevo/', entrenador_create, name='entrenador_create'),
    path('entrenador/<int:pk>/editar/', entrenador_update, name='entrenador_update'),
    path('entrenador/<int:pk>/eliminar/', entrenador_delete, name='entrenador_delete'),

    path('<slug:slug>/posts/nuevo/', post_create, name='clubpost_create'),
    path('posts/<int:pk>/editar/', post_update, name='clubpost_update'),
    path('posts/<int:pk>/eliminar/', post_delete, name='clubpost_delete'),
    path('posts/<int:pk>/responder/', post_reply, name='clubpost_reply'),
    path('posts/<int:pk>/like/', post_toggle_like, name='clubpost_like'),

    path('reserva/<int:pk>/cancelar/', cancel_booking, name='cancel_booking'),

    # El perfil público ahora se maneja desde config.urls con la ruta '@slug'

]

