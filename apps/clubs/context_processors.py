from django.db.models import Q

from .models import ClubMessage


def user_messages(request):
    if not request.user.is_authenticated:
        return {"user_messages": []}

    msgs = (
        ClubMessage.objects.filter(
            (
                Q(user=request.user, sender_is_club=True)
                | Q(club__owner=request.user, sender_is_club=False)
            )
            & Q(is_read=False)
        )
        .select_related("club", "user")
    )
    return {"user_messages": msgs}
