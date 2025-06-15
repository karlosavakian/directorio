from django.db import models
from .club import Club    


class Competidor(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='competidores')
    nombre = models.CharField(max_length=100)
    victorias = models.IntegerField(default=0)
    derrotas = models.IntegerField(default=0)
    empates = models.IntegerField(default=0)
    titulos = models.TextField(blank=True)

    def __str__(self):
        return self.nombre
