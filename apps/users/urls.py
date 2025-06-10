from django.urls import path
from .views import public, review
from .views import profile as profile_views
from django.contrib.auth import views as auth_views 
from .views import auth
from .forms import *

 
urlpatterns = [ 

    
    path('register/', auth.register, name='register'),
    path('accounts/login/', auth_views.LoginView.as_view(
        template_name='users/login.html', 
        authentication_form=LoginForm
    ), name='login'),
    path('profile/', profile_views.profile, name='profile'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', auth.register, name='register'),

    
    path('reseña/<slug:slug>/', review.dejar_reseña, name='dejar-reseña'),  # Dejar Reseña
    path('club/<slug:slug>/editar_reseña/<int:reseña_id>/', review.editar_reseña, name='editar_reseña'),
    path('reseña/<int:reseña_id>/eliminar/', review.eliminar_reseña, name='eliminar-reseña'),
    path('mis-reseñas/', review.mis_reseñas, name='mis-reseñas'),     # Mis Reseñas
]

