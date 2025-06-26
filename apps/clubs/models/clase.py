from .club import Club
from .horario import Horario
from django.db import models



class Clase(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='clases')
    dia = models.CharField(max_length=10, choices=Horario.DiasSemana.choices)
    nombre = models.CharField(max_length=100)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    nota = models.CharField(max_length=20, blank=True)

    def __str__(self):
        texto = f"{self.hora_inicio} - {self.hora_fin}"
        if self.nota:
            texto += f" ({self.nota})"
        return f"{self.nombre} - {self.get_dia_display()} {texto}"

