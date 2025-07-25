from django.db import models
from django.contrib.auth.models import User
from .post import ClubPost
from .club import Club
from .booking_class import BookingClass


class Booking(models.Model):
    STATUS_CHOICES = [
        ('active', 'Activa'),
        ('cancelled', 'Cancelada'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='bookings', null=True, blank=True)
    evento = models.ForeignKey(ClubPost, on_delete=models.CASCADE, null=True, blank=True, related_name='bookings')
    fecha = models.DateField(null=True, blank=True)
    hora = models.TimeField(null=True, blank=True)
    class_type = models.ForeignKey(
        BookingClass,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='bookings'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.evento:
            item = self.evento.titulo
        else:
            item = self.class_type.titulo if self.class_type else 'Clase'
        fecha = self.fecha.isoformat() if self.fecha else 'sin fecha'
        hora = self.hora.strftime('%H:%M') if self.hora else '--:--'
        return f"{self.user.username} - {item} {fecha} {hora} ({self.status})"
