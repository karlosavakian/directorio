from django.db import models
from .club import Club

class ScheduleHour(models.Model):
    """Store available booking hours for a club."""
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='schedule_hours')
    hora = models.TimeField()

    class Meta:
        unique_together = ('club', 'hora')
        ordering = ['hora']

    def __str__(self):
        return f"{self.club.name} {self.hora.strftime('%H:%M')}"
