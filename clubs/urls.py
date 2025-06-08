
# clubs/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('resultados/', views.search_results, name='search_results'), 
    path('@<slug:slug>/', views.club_profile, name='club_profile'),
    path('reseña/<int:reseña_id>/editar/', views.editar_reseña, name='editar_reseña'),
    path('reseña/<int:reseña_id>/eliminar/', views.eliminar_reseña, name='eliminar_reseña'),
    path('mis-reseñas/', views.mis_reseñas, name='mis_reseñas'),

    
]
 
 