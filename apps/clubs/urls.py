# apps/clubs/urls.py

from django.urls import path
from .views import (
    dashboard, 
    search,
    public, 
)

urlpatterns = [                       
    path('resultados/', search.search_results, name='search_results'),  
    path('<slug:slug>/', public.club_profile, name='club_profile'),    
 
]


 