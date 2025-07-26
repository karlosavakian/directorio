from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Max, Q

from ..models import Club, ClubMessage
from ..forms import ClubMessageForm


@login_required
def message_inbox(request):
    """Display the latest message of each conversation."""
    latest_ids = (
        ClubMessage.objects.filter(
            Q(user=request.user) | Q(club__owner=request.user)
        )
        .values('club', 'user')
        .annotate(last_id=Max('id'))
        .values_list('last_id', flat=True)
    )
    conversations = (
        ClubMessage.objects.filter(id__in=latest_ids)
        .select_related('club', 'user')
        .order_by('-created_at')
    )
    return render(request, 'clubs/message_inbox.html', {'conversations': conversations})


@login_required
def conversation(request, slug, user_id=None):
    """Conversation between a user and a club."""
    club = get_object_or_404(Club, slug=slug)

    if request.user == club.owner and user_id is not None:
        conversant = get_object_or_404(User, pk=user_id)
    else:
        conversant = request.user

    messages_qs = (
        ClubMessage.objects.filter(club=club, user=conversant)
        .select_related('user')
        .order_by('created_at')
    )

    if request.method == 'POST':
        form = ClubMessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.club = club
            msg.user = conversant
            msg.sender_is_club = request.user == club.owner
            msg.save()
            if request.user == club.owner:
                return redirect('club_conversation', slug=club.slug, user_id=conversant.id)
            return redirect('conversation', slug=club.slug)
    else:
        form = ClubMessageForm()

    context = {
        'club': club,
        'messages': messages_qs,
        'form': form,
        'conversant': conversant,
    }
    return render(request, 'clubs/conversation.html', context)
