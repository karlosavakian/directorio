from django.urls import path
from django.contrib.auth import views as auth_views

from .views import auth, review, follow
from .views import profile as profile_views
from .views.auth import LoginView

urlpatterns = [
    # Registro de usuarios
    path('signup/', auth.register, name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('perfil/', profile_views.profile, name='profile'),
    path('perfil/planes/', profile_views.plans, name='profile_plans'),
    path('reseña/<slug:slug>/', review.dejar_reseña, name='dejar-reseña'),
  
    path('reseña/<int:reseña_id>/editar/', review.editar_reseña, name='editar_reseña'),
    path('reseña/<int:reseña_id>/eliminar/', review.eliminar_reseña, name='eliminar_reseña'),
    path('follow/<str:model>/<int:object_id>/', follow.toggle_follow, name='toggle_follow'),
    path('eliminar-cuenta/', profile_views.delete_account, name='delete_account'),
]
