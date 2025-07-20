from django.db import models
from django.contrib.auth.models import User

from .club import Club


class ClassReservation(models.Model):
    class ClassType(models.TextChoices):
        PRUEBA = 'prueba', 'Clase de prueba'
        PRIVADA = 'privada', 'Clase privada'

    class Status(models.TextChoices):
        ACTIVE = 'active', 'Activa'
        CANCELLED = 'cancelled', 'Cancelada'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='class_reservations')
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='class_reservations')
    class_type = models.CharField(max_length=20, choices=ClassType.choices)
    date = models.DateField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.get_class_type_display()} ({self.date})"
