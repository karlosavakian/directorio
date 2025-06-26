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
    book_clase,
    cancel_booking,
)
from apps.clubs.views.dashboard import (
    dashboard,
    club_edit,
    clase_create,
    clase_update,
    clase_delete,
    photo_upload,
    photo_delete,
    horario_create,
    horario_update,
    horario_delete,
    horario_clase_create,
    horario_clase_update,
    horario_clase_delete,
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
    path('<slug:slug>/clase/nueva/', clase_create, name='clase_create'),
    path('clase/<int:pk>/editar/', clase_update, name='clase_update'),
    path('clase/<int:pk>/eliminar/', clase_delete, name='clase_delete'),

    path('<slug:slug>/foto/nueva/', photo_upload, name='clubphoto_upload'),
    path('foto/<int:pk>/eliminar/', photo_delete, name='clubphoto_delete'),

    path('<slug:slug>/horario/nuevo/', horario_create, name='horario_create'),
    path('horario/<int:pk>/editar/', horario_update, name='horario_update'),
    path('horario/<int:pk>/eliminar/', horario_delete, name='horario_delete'),
    path('horario/<int:horario_id>/clase/nueva/', horario_clase_create, name='horario_clase_create'),
    path('horario/clase/<int:pk>/editar/', horario_clase_update, name='horario_clase_update'),
    path('horario/clase/<int:pk>/eliminar/', horario_clase_delete, name='horario_clase_delete'),

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

    path('clase/<int:clase_id>/reservar/', book_clase, name='book_clase'),
    path('reserva/<int:pk>/cancelar/', cancel_booking, name='cancel_booking'),

    # El perfil público ahora se maneja desde config.urls con la ruta '@slug'

]

