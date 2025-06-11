from django.db import models
from django.contrib.auth.models import User

VALORACION_CHOICES = [(i, str(i)) for i in range(1, 6)]

class Reseña(models.Model):
    club = models.ForeignKey('Club', on_delete=models.CASCADE, related_name='reseñas')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    instalaciones = models.PositiveIntegerField(choices=VALORACION_CHOICES)
    entrenadores = models.PositiveIntegerField(choices=VALORACION_CHOICES)
    ambiente = models.PositiveIntegerField(choices=VALORACION_CHOICES)
    calidad_precio = models.PositiveIntegerField(choices=VALORACION_CHOICES)
    variedad_clases = models.PositiveIntegerField(choices=VALORACION_CHOICES)
    
    comentario = models.TextField(blank=True)
    creado = models.DateTimeField(auto_now_add=True)

    def promedio(self):
        return round((
            self.instalaciones + self.entrenadores +
            self.ambiente + self.calidad_precio + self.variedad_clases
        ) / 5, 1)

    def __str__(self):
        return f"{self.usuario.username} - {self.club.name} ({self.promedio()}⭐)"
    @property
    def average_rating(self):
        reseñas = self.reseñas.all()
        if not reseñas.exists():
            return None
        total = sum([r.promedio() for r in reseñas])
        return round(total / reseñas.count(), 1)

    @property
    def reviews_count(self):
        return self.reseñas.count()
