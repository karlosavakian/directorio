from django.db import models
from .club import Club

class Entrenador(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='entrenadores')
    avatar = models.ImageField(upload_to='entrenadores/', blank=True, null=True)
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"
