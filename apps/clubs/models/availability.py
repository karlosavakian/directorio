from django.db import models
from .club import Club

class AvailabilitySlot(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='availability')
    date = models.DateField()
    time = models.TimeField()
    slots = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('club', 'date', 'time')
        ordering = ['date', 'time']

    def __str__(self):
        return f"{self.club.name} {self.date} {self.time} ({self.slots})"
