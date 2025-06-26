from django.db import models

from .club import Club


class Horario(models.Model):
    class DiaSemana(models.TextChoices):
        LUNES = 'lunes', 'Lunes'
        MARTES = 'martes', 'Martes'
        MIERCOLES = 'miercoles', 'Miércoles'
        JUEVES = 'jueves', 'Jueves'
        VIERNES = 'viernes', 'Viernes'
        SABADO = 'sabado', 'Sábado'
        DOMINGO = 'domingo', 'Domingo'

    club = models.ForeignKey(Club, related_name='horarios', on_delete=models.CASCADE)
    dia = models.CharField(max_length=10, choices=DiaSemana.choices)
    abierto = models.BooleanField(default=False)
    hora_inicio = models.TimeField(blank=True, null=True)
    hora_fin = models.TimeField(blank=True, null=True)
    nota = models.CharField(max_length=30, blank=True)

    class Meta:
        unique_together = ('club', 'dia')
        ordering = ['dia']

    def __str__(self) -> str:
        return f"{self.get_dia_display()} - {'Abierto' if self.abierto else 'Cerrado'}"
