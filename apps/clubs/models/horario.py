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

    ESTADO_CHOICES = [
        ('abierto', _('Abierto')),
        ('cerrado', _('Cerrado')),
    ]

    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='horarios')
    dia = models.CharField(max_length=10, choices=DiasSemana.choices)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    estado = models.CharField(
        max_length=10,
        choices=ESTADO_CHOICES,
        default='abierto'
    )

    class Meta:
        ordering = ['dia', 'hora_inicio']

    def __str__(self):
        status = dict(self.ESTADO_CHOICES).get(self.estado, self.estado)
        if self.estado == 'cerrado':
            time_range = _('Cerrado')
        else:
            time_range = f"{self.hora_inicio} - {self.hora_fin}"
        return f"{self.club.name} - {self.get_dia_display()} {time_range} ({status})"
