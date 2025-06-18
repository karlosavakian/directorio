from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.db.models import Q

from ..models import (
    Club,
    Clase,
    ClubPost,
    Booking,
    ClubPhoto,
    Horario,
    Competidor,
    Entrenador,
)
from ..forms import (
    ClubForm,
    ClaseForm,
    ClubPostForm,
    ClubPhotoForm,
    HorarioForm,
    CompetidorForm,
    EntrenadorForm,
)
from ..permissions import has_club_permission


@login_required
def dashboard(request, slug):
    club = get_object_or_404(Club, slug=slug)
    if club.owner != request.user:
        return redirect('home')
    classes = club.clases.all()
    coaches = club.entrenadores.all()
    posts = club.posts.all()
    bookings = Booking.objects.filter(
        Q(clase__club=club) | Q(evento__club=club)
    ).select_related('user', 'clase', 'evento')

    form = ClubForm(instance=club)

    return render(
        request,
        'clubs/dashboard.html',
        {
            'club': club,
            'classes': classes,
            'posts': posts,
            'bookings': bookings,
            'form': form,
            'coaches': coaches,
        },
    )


@login_required
def club_edit(request, slug):
    club = get_object_or_404(Club, slug=slug)
    if not has_club_permission(request.user, club):
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = ClubForm(request.POST, request.FILES, instance=club)
        if form.is_valid():
            form.save()
            messages.success(request, 'Club actualizado correctamente.')
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
            messages.success(request, 'Clase creada correctamente.')
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
            messages.success(request, 'Clase actualizada correctamente.')
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
        messages.success(request, 'Clase eliminada correctamente.')
        return redirect('club_dashboard', slug=slug)
    return render(request, 'clubs/clase_confirm_delete.html', {'clase': clase})


@login_required
def photo_upload(request, slug):
    club = get_object_or_404(Club, slug=slug)
    if not has_club_permission(request.user, club):
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = ClubPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.club = club
            photo.save()
            messages.success(request, 'Foto añadida correctamente.')
            return redirect('club_dashboard', slug=club.slug)
    else:
        form = ClubPhotoForm()
    return render(request, 'clubs/photo_form.html', {'form': form, 'club': club})


@login_required
def photo_delete(request, pk):
    photo = get_object_or_404(ClubPhoto, pk=pk)
    if not has_club_permission(request.user, photo.club):
        return HttpResponseForbidden()
    if request.method == 'POST':
        slug = photo.club.slug
        photo.delete()
        messages.success(request, 'Foto eliminada correctamente.')
        return redirect('club_dashboard', slug=slug)
    return render(request, 'clubs/photo_confirm_delete.html', {'photo': photo})


@login_required
def horario_create(request, slug):
    club = get_object_or_404(Club, slug=slug)
    if not has_club_permission(request.user, club):
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = HorarioForm(request.POST)
        if form.is_valid():
            horario = form.save(commit=False)
            horario.club = club
            horario.save()
            messages.success(request, 'Horario añadido correctamente.')
            return redirect('club_dashboard', slug=club.slug)
    else:
        form = HorarioForm()
    return render(request, 'clubs/horario_form.html', {'form': form, 'club': club})


@login_required
def horario_update(request, pk):
    horario = get_object_or_404(Horario, pk=pk)
    if not has_club_permission(request.user, horario.club):
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = HorarioForm(request.POST, instance=horario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Horario actualizado correctamente.')
            return redirect('club_dashboard', slug=horario.club.slug)
    else:
        form = HorarioForm(instance=horario)
    return render(request, 'clubs/horario_form.html', {
        'form': form,
        'club': horario.club,
        'horario': horario,
    })


@login_required
def horario_delete(request, pk):
    horario = get_object_or_404(Horario, pk=pk)
    if not has_club_permission(request.user, horario.club):
        return HttpResponseForbidden()
    if request.method == 'POST':
        slug = horario.club.slug
        horario.delete()
        messages.success(request, 'Horario eliminado correctamente.')
        return redirect('club_dashboard', slug=slug)
    return render(request, 'clubs/horario_confirm_delete.html', {'horario': horario})


@login_required
def competidor_create(request, slug):
    club = get_object_or_404(Club, slug=slug)
    if not has_club_permission(request.user, club):
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = CompetidorForm(request.POST, request.FILES)
        if form.is_valid():
            competidor = form.save(commit=False)
            competidor.club = club
            competidor.save()
            messages.success(request, 'Competidor añadido correctamente.')
            return redirect('club_dashboard', slug=club.slug)
    else:
        form = CompetidorForm()
    return render(request, 'clubs/competidor_form.html', {'form': form, 'club': club})


@login_required
def competidor_update(request, pk):
    competidor = get_object_or_404(Competidor, pk=pk)
    if not has_club_permission(request.user, competidor.club):
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = CompetidorForm(request.POST, request.FILES, instance=competidor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Competidor actualizado correctamente.')
            return redirect('club_dashboard', slug=competidor.club.slug)
    else:
        form = CompetidorForm(instance=competidor)
    return render(request, 'clubs/competidor_form.html', {
        'form': form,
        'club': competidor.club,
        'competidor': competidor,
    })


@login_required
def competidor_delete(request, pk):
    competidor = get_object_or_404(Competidor, pk=pk)
    if not has_club_permission(request.user, competidor.club):
        return HttpResponseForbidden()
    if request.method == 'POST':
        slug = competidor.club.slug
        competidor.delete()
        messages.success(request, 'Competidor eliminado correctamente.')
        return redirect('club_dashboard', slug=slug)
    return render(request, 'clubs/competidor_confirm_delete.html', {
        'competidor': competidor,
    })


@login_required
def entrenador_create(request, slug):
    club = get_object_or_404(Club, slug=slug)
    if not has_club_permission(request.user, club):
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = EntrenadorForm(request.POST, request.FILES)
        if form.is_valid():
            entrenador = form.save(commit=False)
            entrenador.club = club
            entrenador.save()
            form.save_m2m()
            messages.success(request, 'Entrenador añadido correctamente.')
            return redirect('club_dashboard', slug=club.slug)
    else:
        form = EntrenadorForm()
    return render(request, 'clubs/entrenador_form.html', {'form': form, 'club': club})


@login_required
def entrenador_update(request, pk):
    entrenador = get_object_or_404(Entrenador, pk=pk)
    if not has_club_permission(request.user, entrenador.club):
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = EntrenadorForm(request.POST, request.FILES, instance=entrenador)
        if form.is_valid():
            form.save()
            messages.success(request, 'Entrenador actualizado correctamente.')
            return redirect('club_dashboard', slug=entrenador.club.slug)
    else:
        form = EntrenadorForm(instance=entrenador)
    return render(request, 'clubs/entrenador_form.html', {
        'form': form,
        'club': entrenador.club,
        'entrenador': entrenador,
    })


@login_required
def entrenador_delete(request, pk):
    entrenador = get_object_or_404(Entrenador, pk=pk)
    if not has_club_permission(request.user, entrenador.club):
        return HttpResponseForbidden()
    if request.method == 'POST':
        slug = entrenador.club.slug
        entrenador.delete()
        messages.success(request, 'Entrenador eliminado correctamente.')
        return redirect('club_dashboard', slug=slug)
    return render(request, 'clubs/entrenador_confirm_delete.html', {
        'entrenador': entrenador,
    })
