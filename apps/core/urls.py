# apps/core/urls.py
from django.urls import path 
from .views import home, ayuda, planes

urlpatterns = [
    path('', home, name='home'),
    path('ayuda/', ayuda, name='ayuda'),
    path('planes/', planes, name='planes'),

]
