# apps/core/urls.py
from django.urls import path 
from .views import home, ayuda, pro, registro_profesional, terminos, privacidad, cookies

urlpatterns = [
    path('', home, name='home'),
    path('ayuda/', ayuda, name='ayuda'),
    path('pro/', pro, name='pro'),
    path('pro/registro/', registro_profesional, name='registro_profesional'),
    path('terminos/', terminos, name='terminos'),
    path('privacidad/', privacidad, name='privacidad'),
    path('cookies/', cookies, name='cookies'),

]
