from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Club, DaySchedule


@receiver(post_save, sender=Club)
def create_day_schedules(sender, instance, created, **kwargs):
    if not created:
        return
    for day, _ in DaySchedule.WeekDay.choices:
        DaySchedule.objects.create(club=instance, day=day, is_open=False)

