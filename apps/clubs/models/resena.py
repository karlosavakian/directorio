from django.db import models
from django.contrib.auth.models import User

VALORACION_CHOICES = [(i, str(i)) for i in range(1, 6)]

class Reseña(models.Model):
    club = models.ForeignKey('Club', on_delete=models.CASCADE, related_name='reseñas')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
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
        return f"{self.titulo} - {self.usuario.username} ({self.promedio()}⭐)"
