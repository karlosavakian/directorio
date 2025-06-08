# apps/clubs/views/review.py

from django.shortcuts import render, get_object_or_404, redirect
from apps.clubs.models import Reseña, Club
from ..forms import ReseñaForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

 


@login_required
def dejar_reseña(request, slug):
    """ Vista para dejar una reseña """
    club = get_object_or_404(Club, slug=slug)

    if request.method == 'POST':
        form = ReseñaForm(request.POST)
        if form.is_valid():
            reseña = form.save(commit=False)
            reseña.club = club
            reseña.usuario = request.user
            reseña.stars = reseña.promedio()  # nota calculada automáticamente
            reseña.save()
            messages.success(request, '¡Gracias por dejar tu reseña!')
            return redirect('club_profile', slug=slug)
    else:
        form = ReseñaForm()

    return render(request, 'clubs/dejar_reseña.html', {
        'club': club,
        'form': form
    })


@login_required
def editar_reseña(request, reseña_id):
    """ Vista para editar una reseña existente """
    reseña = get_object_or_404(Reseña, id=reseña_id, usuario=request.user)
    if request.method == 'POST':
        form = ReseñaForm(request.POST, instance=reseña)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Reseña actualizada exitosamente!')
            return redirect('club_profile', slug=reseña.club.slug)
    else:
        form = ReseñaForm(instance=reseña)

    return render(request, 'clubs/editar_reseña.html', {
        'form': form,
        'reseña': reseña
    })


@login_required
def eliminar_reseña(request, reseña_id):
    """ Vista para eliminar una reseña """
    reseña = get_object_or_404(Reseña, id=reseña_id, usuario=request.user)
    club_slug = reseña.club.slug
    if request.method == 'POST':
        reseña.delete()
        messages.success(request, '¡Reseña eliminada exitosamente!')
        return redirect('club_profile', slug=club_slug)

    return render(request, 'clubs/eliminar_reseña.html', {
        'reseña': reseña
    })


@login_required
def mis_reseñas(request):
    """ Vista para listar todas las reseñas de un usuario """
    reseñas = Reseña.objects.filter(usuario=request.user)
    return render(request, 'clubs/mis_reseñas.html', {
        'reseñas': reseñas
    })
