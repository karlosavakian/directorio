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
    create_booking,
    booking_confirm,
    booking_cancel_admin,
    booking_delete,
)
from apps.clubs.views.dashboard import (
    dashboard,
    photo_upload,
    photo_delete,
    photo_bulk_delete,
    photo_set_main,
    horario_create,
    horario_update,
    horario_delete,
    competidor_create,
    competidor_update,
    competidor_delete,
    entrenador_create,
    entrenador_update,
    entrenador_delete,
    miembro_create,
    miembro_update,
    miembro_detail,
    miembro_delete,
    miembro_pagos,
    pago_create,
    pago_update,
    pago_delete,
    schedule_hours,
    miembros_json,
    booking_class_create,
    booking_class_update,
    booking_class_delete,
    check_slug,
    cities_by_country,
    matchmaker_toggle_bookmark,
)

urlpatterns = [
    path('resultados/', search.search_results, name='search_results'),
    path('valoraciones/<slug:slug>/', public.ajax_reviews, name='ajax_reviews'),
    path('slug-disponible/', check_slug, name='club_slug_check'),
    path('ciudades/', cities_by_country, name='cities_by_country'),

    path('<slug:slug>/foto/nueva/', photo_upload, name='clubphoto_upload'),
    path('foto/<int:pk>/eliminar/', photo_delete, name='clubphoto_delete'),
    path('<slug:slug>/foto/eliminar/', photo_bulk_delete, name='clubphoto_bulk_delete'),
    path('foto/<int:pk>/principal/', photo_set_main, name='clubphoto_set_main'),

    path('<slug:slug>/horario/nuevo/', horario_create, name='horario_create'),
    path('horario/<int:pk>/editar/', horario_update, name='horario_update'),
    path('horario/<int:pk>/eliminar/', horario_delete, name='horario_delete'),

    path('<slug:slug>/competidor/nuevo/', competidor_create, name='competidor_create'),
    path('competidor/<int:pk>/editar/', competidor_update, name='competidor_update'),
    path('competidor/<int:pk>/eliminar/', competidor_delete, name='competidor_delete'),
    path('<slug:slug>/miembros/json/', miembros_json, name='miembros_json'),

    path('<slug:slug>/entrenador/nuevo/', entrenador_create, name='entrenador_create'),
    path('entrenador/<int:pk>/editar/', entrenador_update, name='entrenador_update'),
    path('entrenador/<int:pk>/eliminar/', entrenador_delete, name='entrenador_delete'),

    path('<slug:slug>/miembro/nuevo/', miembro_create, name='miembro_create'),
    path('miembro/<int:pk>/editar/', miembro_update, name='miembro_update'),
    path('miembro/<int:pk>/detalle/', miembro_detail, name='miembro_detail'),
    path('miembro/<int:pk>/eliminar/', miembro_delete, name='miembro_delete'),
    path('miembro/<int:pk>/pagos/', miembro_pagos, name='miembro_pagos'),
    path('miembro/<int:miembro_id>/pago/nuevo/', pago_create, name='pago_create'),
    path('pago/<int:pk>/editar/', pago_update, name='pago_update'),
    path('pago/<int:pk>/eliminar/', pago_delete, name='pago_delete'),

    path('<slug:slug>/posts/nuevo/', post_create, name='clubpost_create'),
    path('posts/<int:pk>/editar/', post_update, name='clubpost_update'),
    path('posts/<int:pk>/eliminar/', post_delete, name='clubpost_delete'),
    path('posts/<int:pk>/responder/', post_reply, name='clubpost_reply'),
    path('posts/<int:pk>/like/', post_toggle_like, name='clubpost_like'),

    path('<slug:slug>/mensaje/', public.send_message, name='club_send_message'),

    path('matchmaker/bookmark/', matchmaker_toggle_bookmark, name='matchmaker_bookmark'),

    path('reserva/<int:pk>/cancelar/', cancel_booking, name='cancel_booking'),
    path('<slug:slug>/reservar/crear/', create_booking, name='create_booking'),
    path('booking/<int:pk>/confirmar/', booking_confirm, name='booking_confirm'),
    path('booking/<int:pk>/cancelar-admin/', booking_cancel_admin, name='booking_cancel_admin'),
    path('booking/<int:pk>/eliminar/', booking_delete, name='booking_delete'),
    path('<slug:slug>/schedule-hours/', schedule_hours, name='schedule_hours'),
    path('<slug:slug>/clase/nueva/', booking_class_create, name='booking_class_create'),
    path('clase/<int:pk>/editar/', booking_class_update, name='booking_class_update'),
    path('clase/<int:pk>/eliminar/', booking_class_delete, name='booking_class_delete'),

    # El perfil público ahora se maneja desde config.urls con la ruta '@slug'

]

