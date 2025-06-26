from django.db import models
from django.utils.translation import gettext_lazy as _  
from .club import Club

    
class Horario(models.Model):
    class DiasSemana(models.TextChoices):
        LUNES = 'lunes', _('Lunes')
        MARTES = 'martes', _('Martes')
        MIERCOLES = 'miercoles', _('Miércoles')
        JUEVES = 'jueves', _('Jueves')
        VIERNES = 'viernes', _('Viernes')
        SABADO = 'sabado', _('Sábado')
        DOMINGO = 'domingo', _('Domingo')

    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='horarios')
    dia = models.CharField(max_length=10, choices=DiasSemana.choices)
    abierto = models.BooleanField(default=False)

    class Meta:
        unique_together = ('club', 'dia')
        ordering = ['dia']

    def __str__(self):
        estado = 'abierto' if self.abierto else 'cerrado'
        return f"{self.club.name} - {self.get_dia_display()} ({estado})"


class HorarioClase(models.Model):
    horario = models.ForeignKey(Horario, on_delete=models.CASCADE, related_name='clases')
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    texto = models.CharField(max_length=30, blank=True)

    class Meta:
        ordering = ['hora_inicio']

    def __str__(self):
        if self.texto:
            return f"{self.horario.get_dia_display()} {self.hora_inicio}-{self.hora_fin} {self.texto}"
        return f"{self.horario.get_dia_display()} {self.hora_inicio}-{self.hora_fin}"
