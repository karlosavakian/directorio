from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User

from apps.clubs.models import Club, Reseña, ClubPost
from ..models import Follow


@login_required
def toggle_follow(request, model, object_id):
    content_type = get_object_or_404(ContentType, model=model)
    follower_ct = ContentType.objects.get_for_model(request.user)
    follow, created = Follow.objects.get_or_create(
        follower_content_type=follower_ct,
        follower_object_id=request.user.id,
        followed_content_type=content_type,
        followed_object_id=object_id,
    )
    if not created:
        follow.delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def feed(request):
    follower_ct = ContentType.objects.get_for_model(request.user)
    follows = Follow.objects.filter(
        follower_content_type=follower_ct,
        follower_object_id=request.user.id,
    )
    posts = []
    ct_user = ContentType.objects.get_for_model(User)
    ct_club = ContentType.objects.get_for_model(Club)
    for f in follows:
        if f.followed_content_type == ct_club:
            posts.extend(Reseña.objects.filter(club_id=f.followed_object_id))
            posts.extend(ClubPost.objects.filter(club_id=f.followed_object_id))
        elif f.followed_content_type == ct_user:
            posts.extend(Reseña.objects.filter(usuario_id=f.followed_object_id))
    posts = sorted(posts, key=lambda r: getattr(r, 'creado', r.created_at), reverse=True)[:20]
    return render(request, 'users/feed.html', {'posts': posts})
