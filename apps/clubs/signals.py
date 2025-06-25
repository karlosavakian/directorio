from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import time

from .models import Club, Horario

@receiver(post_save, sender=Club)
def create_default_horarios(sender, instance, created, **kwargs):
    if created and not instance.horarios.exists():
        for dia, _ in Horario.DiasSemana.choices:
            Horario.objects.create(
                club=instance,
                dia=dia,
                estado=Horario.Estado.ABIERTO,
                hora_inicio=time(9, 0),
                hora_fin=time(17, 0),
            )
