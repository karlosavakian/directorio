# apps/core/views.py
from django.shortcuts import render

 
def home(request):
    search_query = request.GET.get('q', '').strip()
    return render(request, 'core/home.html', {
        'search_query': search_query,
    })
 
 
