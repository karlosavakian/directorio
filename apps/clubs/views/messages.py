from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Max, Q, Subquery, OuterRef
from django.http import JsonResponse

from ..models import Club, ClubMessage, ClubChat
from ..forms import ClubMessageForm
from apps.core.templatetags.utils_filters import message_timestamp


@login_required
def conversation(request, chat_id=None):
    """Display inbox or a conversation based on query params or chat ID."""
    slug = request.GET.get('club')
    user_id = request.GET.get('user')

    ClubMessage.objects.filter(
        (
            Q(user=request.user, sender_is_club=True)
            | Q(club__owner=request.user, sender_is_club=False)
        )
        & Q(is_read=False)
    ).update(is_read=True)

    latest_ids = (
        ClubMessage.objects.filter(
            Q(user=request.user) | Q(club__owner=request.user)
        )
        .values('club', 'user')
        .annotate(last_id=Max('id'))
        .values_list('last_id', flat=True)
    )
    chat_id_sub = Subquery(
        ClubChat.objects.filter(club=OuterRef('club'), user=OuterRef('user')).values('chat_id')[:1]
    )
    conversations = (
        ClubMessage.objects.filter(id__in=latest_ids)
        .select_related('club', 'user')
        .annotate(chat_id=chat_id_sub)
        .order_by('-created_at')
    )

    club = None
    conversant = None
    messages_qs = ClubMessage.objects.none()
    form = None

    if chat_id:
        chat = get_object_or_404(ClubChat, chat_id=chat_id)
        club = chat.club
        conversant = chat.user if request.user == club.owner else request.user
        messages_qs = (
            ClubMessage.objects.filter(club=club, user=chat.user)
            .select_related('user', 'reply_to')
            .order_by('created_at')
        )
        unread_filter = Q(is_read=False)
        if request.user == club.owner:
            unread_filter &= Q(sender_is_club=False)
        else:
            unread_filter &= Q(sender_is_club=True)
        messages_qs.filter(unread_filter).update(is_read=True)
    elif slug:
        club = get_object_or_404(Club, slug=slug)
        if request.user == club.owner and user_id is not None:
            conversant = get_object_or_404(User, pk=user_id)
        else:
            conversant = request.user
        chat, _ = ClubChat.objects.get_or_create(club=club, user=conversant)
        return redirect(reverse('chat', args=[chat.chat_id]))
    else:
        context = {
            'club': club,
            'conversant': conversant,
            'messages': messages_qs,
            'form': form,
            'conversations': conversations,
        }
        return render(request, 'clubs/conversation.html', context)

    if request.method == 'POST':
        form = ClubMessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.club = club
            msg.user = chat.user
            msg.sender_is_club = request.user == club.owner
            msg.is_read = True
            msg.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                data = {
                    'id': msg.pk,
                    'content': msg.content,
                    'created_at': message_timestamp(msg.created_at),
                    'sender_is_club': msg.sender_is_club,
                    'like_url': reverse('message_like', args=[msg.pk]),
                    'sender': msg.club.name if msg.sender_is_club else msg.user.username,
                    'reply_to': (
                        {
                            'content': msg.reply_to.content,
                            'sender': msg.reply_to.club.name if msg.reply_to.sender_is_club else msg.reply_to.user.username,
                        }
                        if msg.reply_to
                        else None
                    ),
                }
                return JsonResponse(data)
            return redirect(reverse('chat', args=[chat.chat_id]))
        elif request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'errors': form.errors}, status=400)
    else:
        form = ClubMessageForm()

    context = {
        'club': club,
        'messages': messages_qs,
        'form': form,
        'conversant': conversant,
        'conversations': conversations,
    }
    return render(request, 'clubs/conversation.html', context)


@login_required
def message_toggle_like(request, pk):
    msg = get_object_or_404(ClubMessage, pk=pk)
    if request.user in msg.likes.all():
        msg.likes.remove(request.user)
        liked = False
    else:
        msg.likes.add(request.user)
        liked = True

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'liked': liked, 'count': msg.likes.count()})

    return redirect(request.META.get('HTTP_REFERER', '/'))
