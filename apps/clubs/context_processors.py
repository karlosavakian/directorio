from django.db.models import Q

from .models import ClubMessage


def user_messages(request):
    if not request.user.is_authenticated:
        return {"user_messages": []}

    msgs = (
        ClubMessage.objects.filter(
            Q(user=request.user) | Q(club__owner=request.user)
        )
        .select_related("club", "user")
    )
    return {"user_messages": msgs}
