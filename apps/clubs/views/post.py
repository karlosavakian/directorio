from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.http import JsonResponse

from ..models import Club, ClubPost
from ..forms import ClubPostForm, ClubPostReplyForm
from ..permissions import has_club_permission


@login_required
def post_create(request, slug):
    club = get_object_or_404(Club, slug=slug)
    # Only the owner of the club is allowed to create new posts
    if request.user != club.owner:
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = ClubPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.club = club
            post.user = request.user
            post.save()
            messages.success(request, 'Publicación creada correctamente.')
            return redirect('club_profile', slug=slug)
    else:
        form = ClubPostForm()
    return render(request, 'clubs/post_form.html', {'form': form, 'club': club})


@login_required
def post_update(request, pk):
    post = get_object_or_404(ClubPost, pk=pk)
    if not (has_club_permission(request.user, post.club) or request.user == post.user):
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = ClubPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Publicación actualizada correctamente.')
            return redirect('club_profile', slug=post.club.slug)
    else:
        form = ClubPostForm(instance=post)
    return render(request, 'clubs/post_form.html', {'form': form, 'club': post.club})


@login_required
def post_delete(request, pk):
    post = get_object_or_404(ClubPost, pk=pk)
    if not (has_club_permission(request.user, post.club) or request.user == post.user):
        return HttpResponseForbidden()
    if request.method == 'POST':
        slug = post.club.slug
        post.delete()
        messages.success(request, 'Publicación eliminada correctamente.')
        return redirect('club_profile', slug=slug)
    return render(request, 'clubs/post_confirm_delete.html', {'post': post})


@login_required
def post_reply(request, pk):
    parent = get_object_or_404(ClubPost, pk=pk)
    if request.method == 'POST':
        form = ClubPostReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.club = parent.club
            reply.parent = parent
            reply.user = request.user
            reply.save()
            messages.success(request, 'Respuesta publicada correctamente.')
            return redirect('club_profile', slug=parent.club.slug)
    else:
        form = ClubPostReplyForm()
    return render(request, 'clubs/post_reply_form.html', {
        'form': form,
        'post': parent,
        'club': parent.club,
    })


@login_required
def post_toggle_like(request, pk):
    post = get_object_or_404(ClubPost, pk=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'liked': liked, 'count': post.likes.count()})

    return redirect('club_profile', slug=post.club.slug)
