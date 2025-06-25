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

    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='horarios')
    dia = models.CharField(max_length=10, choices=DiasSemana.choices)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    estado = models.CharField(
        max_length=8, choices=Estado.choices, default=Estado.ABIERTO
    )
    comentario = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['dia', 'hora_inicio']

    def __str__(self):
        if self.estado == self.Estado.CERRADO:
            status = _('Cerrado')
        else:
            status = f"{self.hora_inicio} - {self.hora_fin}"
        return f"{self.club.name} - {self.get_dia_display()} {status}"
