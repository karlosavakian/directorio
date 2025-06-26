from django.db import models
from django.contrib.auth.models import User
from .post import ClubPost


class Booking(models.Model):
    STATUS_CHOICES = [
        ('active', 'Activa'),
        ('cancelled', 'Cancelada'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    evento = models.ForeignKey(ClubPost, on_delete=models.CASCADE, null=True, blank=True, related_name='bookings')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        item = self.evento.titulo if self.evento else 'Sin referencia'
        return f"{self.user.username} - {item} ({self.status})"
