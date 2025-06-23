from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.models import User

from apps.clubs.models import Club, Reseña, ClubPost
from apps.clubs.forms import ClubPostReplyForm
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
        following = False
        msg = 'Has dejado de seguir este club.'
    else:
        following = True
        msg = 'Ahora sigues este club.'

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'following': following, 'message': msg})

    messages.success(request, msg)

    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def feed(request):
    follower_ct = ContentType.objects.get_for_model(request.user)
    follows = Follow.objects.filter(
        follower_content_type=follower_ct,
        follower_object_id=request.user.id,
    )

    ct_user = ContentType.objects.get_for_model(User)
    ct_club = ContentType.objects.get_for_model(Club)

    club_ids = []
    user_ids = []
    for f in follows:
        if f.followed_content_type_id == ct_club.id:
            club_ids.append(f.followed_object_id)
        elif f.followed_content_type_id == ct_user.id:
            user_ids.append(f.followed_object_id)

    posts = list(
        Reseña.objects
        .select_related("usuario__profile", "club")
        .filter(models.Q(club_id__in=club_ids) | models.Q(usuario_id__in=user_ids))
    )
    posts += list(
        ClubPost.objects.select_related("club", "user").filter(
            models.Q(club_id__in=club_ids) | models.Q(user_id__in=user_ids),
            parent__isnull=True,
        )
    )
    posts = sorted(posts, key=lambda r: getattr(r, 'creado', r.created_at), reverse=True)[:20]
    reply_form = ClubPostReplyForm()
    return render(request, 'users/feed.html', {'posts': posts, 'reply_form': reply_form})
