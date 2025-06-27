# apps/core/urls.py
from django.urls import path 
from .views import home, prelaunch

urlpatterns = [
    path('', home, name='home'),
    path('prelaunch/', prelaunch, name='prelaunch'),

]
