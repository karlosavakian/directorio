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
    estado = models.CharField(max_length=10, choices=Estado.choices, default=Estado.ABIERTO)
    hora_inicio = models.TimeField(blank=True, null=True)
    hora_fin = models.TimeField(blank=True, null=True)

    class Meta:
        ordering = ['dia', 'hora_inicio']

    def __str__(self):
        estado = self.get_estado_display()
        if self.estado == self.Estado.CERRADO:
            return f"{self.club.name} - {self.get_dia_display()} ({estado})"
        return f"{self.club.name} - {self.get_dia_display()} {self.hora_inicio} - {self.hora_fin} ({estado})"
