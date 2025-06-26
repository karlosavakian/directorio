from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Club, Horario


@receiver(post_save, sender=Club)
def create_default_schedule(sender, instance, created, **kwargs):
    if created:
        for dia, _ in Horario.DiaSemana.choices:
            Horario.objects.create(club=instance, dia=dia)
