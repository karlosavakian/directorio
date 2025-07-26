from django.db import models
from django.contrib.auth.models import User

from .club import Club
from apps.core.models import TimeStampedModel


class ClubMessage(TimeStampedModel):
    club = models.ForeignKey(Club, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='club_messages', on_delete=models.CASCADE)
    content = models.TextField()
    sender_is_club = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        sender = self.club.name if self.sender_is_club else self.user.username
        return f"{sender}: {self.content[:20]}"
