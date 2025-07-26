from .models import ClubMessage


def user_messages(request):
    if request.user.is_authenticated:
        msgs = ClubMessage.objects.filter(user=request.user).select_related('club')
    else:
        msgs = []
    return {'user_messages': msgs}
