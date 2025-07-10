# apps/core/urls.py
from django.urls import path 
from .views import home, ayuda

urlpatterns = [
    path('', home, name='home'),
    path('ayuda/', ayuda, name='ayuda'),

]
