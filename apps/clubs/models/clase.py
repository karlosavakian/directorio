from .club import Club    
from django.db import models



class Clase(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='clases')
    nombre = models.CharField(max_length=100)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    def __str__(self):
        return f"{self.nombre} ({self.hora_inicio} - {self.hora_fin})"

