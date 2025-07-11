# apps/core/urls.py
from django.urls import path 
from .views import (
    home,
    ayuda,
    planes,
    terminos,
    privacidad,
    cookies,
    professional_register,
)

urlpatterns = [
    path('', home, name='home'),
    path('ayuda/', ayuda, name='ayuda'),
    path('planes/', planes, name='planes'),
    path('planes/registro/', professional_register, name='professional_register'),
    path('terminos/', terminos, name='terminos'),
    path('privacidad/', privacidad, name='privacidad'),
    path('cookies/', cookies, name='cookies'),

]
