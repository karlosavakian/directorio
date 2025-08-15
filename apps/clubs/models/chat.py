import random
from django.db import models
from django.contrib.auth.models import User
from .club import Club


def generate_chat_id():
    return ''.join(str(random.randint(0, 9)) for _ in range(16))


class ClubChat(models.Model):
    chat_id = models.CharField(max_length=16, unique=True, default=generate_chat_id, editable=False)
    club = models.ForeignKey(Club, related_name='chats', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='chats', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('club', 'user')
