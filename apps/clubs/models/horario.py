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

    class Estado(models.TextChoices):
        ABIERTO = 'abierto', _('Abierto')
        CERRADO = 'cerrado', _('Cerrado')
        VACACIONES = 'vacaciones', _('Vacaciones')
        COMPETICION = 'competicion', _('Competición')

    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='horarios')
    dia = models.CharField(max_length=10, choices=DiasSemana.choices)
    estado = models.CharField(max_length=12, choices=Estado.choices, default=Estado.ABIERTO)

    class Meta:
        ordering = ['dia']
        constraints = [
            models.UniqueConstraint(fields=['club', 'dia'], name='unique_club_day')
        ]

    def __str__(self):
        estado = self.get_estado_display()
        return f"{self.club.name} - {self.get_dia_display()} ({estado})"
