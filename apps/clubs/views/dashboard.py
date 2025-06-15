# Vistas privadas para usuarios autenticados, gestión de contenido, etc.

from django.shortcuts import render
from apps.clubs.models import Club

def dashboard_view(request):
    """ Vista del panel de control """
    clubs = Club.objects.all()
    return render(request, 'clubs/dashboard.html', {
        'clubs': clubs
    })
