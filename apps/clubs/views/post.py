from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from ..models import Club, ClubPost
from ..forms import ClubPostForm


@login_required
def post_create(request, slug):
    club = get_object_or_404(Club, slug=slug)
    if request.method == 'POST':
        form = ClubPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.club = club
            post.save()
            return redirect('club_profile', slug=slug)
    else:
        form = ClubPostForm()
    return render(request, 'clubs/post_form.html', {'form': form, 'club': club})


@login_required
def post_update(request, pk):
    post = get_object_or_404(ClubPost, pk=pk)
    if request.method == 'POST':
        form = ClubPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('club_profile', slug=post.club.slug)
    else:
        form = ClubPostForm(instance=post)
    return render(request, 'clubs/post_form.html', {'form': form, 'club': post.club})


@login_required
def post_delete(request, pk):
    post = get_object_or_404(ClubPost, pk=pk)
    if request.method == 'POST':
        slug = post.club.slug
        post.delete()
        return redirect('club_profile', slug=slug)
    return render(request, 'clubs/post_confirm_delete.html', {'post': post})
