from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.db.models import Q

from ..models import Club, Clase, ClubPost, Booking
from ..forms import ClubForm, ClaseForm, ClubPostForm
from ..permissions import has_club_permission


@login_required
def dashboard(request, slug):
    club = get_object_or_404(Club, slug=slug)
    if not has_club_permission(request.user, club):
        return HttpResponseForbidden()
    classes = club.clases.all()
    posts = club.posts.all()
    bookings = Booking.objects.filter(
        Q(clase__club=club) | Q(evento__club=club)
    ).select_related('user', 'clase', 'evento')
    return render(request, 'clubs/dashboard.html', {
        'club': club,
        'classes': classes,
        'posts': posts,
        'bookings': bookings,
    })


@login_required
def club_edit(request, slug):
    club = get_object_or_404(Club, slug=slug)
    if not has_club_permission(request.user, club):
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = ClubForm(request.POST, request.FILES, instance=club)
        if form.is_valid():
            form.save()
            return redirect('club_dashboard', slug=club.slug)
    else:
        form = ClubForm(instance=club)
    return render(request, 'clubs/club_form.html', {'form': form, 'club': club})


@login_required
def clase_create(request, slug):
    club = get_object_or_404(Club, slug=slug)
    if not has_club_permission(request.user, club):
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = ClaseForm(request.POST)
        if form.is_valid():
            clase = form.save(commit=False)
            clase.club = club
            clase.save()
            return redirect('club_dashboard', slug=club.slug)
    else:
        form = ClaseForm()
    return render(request, 'clubs/clase_form.html', {'form': form, 'club': club})


@login_required
def clase_update(request, pk):
    clase = get_object_or_404(Clase, pk=pk)
    if not has_club_permission(request.user, clase.club):
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = ClaseForm(request.POST, instance=clase)
        if form.is_valid():
            form.save()
            return redirect('club_dashboard', slug=clase.club.slug)
    else:
        form = ClaseForm(instance=clase)
    return render(request, 'clubs/clase_form.html', {'form': form, 'club': clase.club, 'clase': clase})


@login_required
def clase_delete(request, pk):
    clase = get_object_or_404(Clase, pk=pk)
    if not has_club_permission(request.user, clase.club):
        return HttpResponseForbidden()
    if request.method == 'POST':
        slug = clase.club.slug
        clase.delete()
        return redirect('club_dashboard', slug=slug)
    return render(request, 'clubs/clase_confirm_delete.html', {'clase': clase})
