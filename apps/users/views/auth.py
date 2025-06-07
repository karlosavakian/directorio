# Vistas para búsqueda de clubes, filtros, etc.
# apps/users/views/auth.py

from django.shortcuts import render, redirect
from django.contrib.auth import login
from ..forms import RegistroUsuarioForm


def register(request):
    """ Vista para registrar un nuevo usuario """
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistroUsuarioForm()
    
    return render(request, 'users/register.html', {
        'form': form
    })
