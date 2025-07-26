from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
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


