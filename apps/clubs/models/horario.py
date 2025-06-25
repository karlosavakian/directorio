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
    estado = models.CharField(max_length=7, choices=Estado.choices, default=Estado.ABIERTO)
    hora_inicio = models.TimeField(null=True, blank=True)
    hora_fin = models.TimeField(null=True, blank=True)
    nota = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ['dia', 'hora_inicio']

    def __str__(self):
        if self.estado == self.Estado.CERRADO:
            horario = _('Cerrado')
        else:
            horario = f"{self.hora_inicio} - {self.hora_fin}"
        return f"{self.club.name} - {self.get_dia_display()} {horario}"

    def clean(self):
        super().clean()
        if self.estado == self.Estado.ABIERTO:
            if not self.hora_inicio:
                raise models.ValidationError({'hora_inicio': _('Este campo es obligatorio cuando el horario está abierto.')})
            if not self.hora_fin:
                raise models.ValidationError({'hora_fin': _('Este campo es obligatorio cuando el horario está abierto.')})

    def save(self, *args, **kwargs):
        if self.hora_inicio:
            self.hora_inicio = self.hora_inicio.replace(second=0, microsecond=0)
        if self.hora_fin:
            self.hora_fin = self.hora_fin.replace(second=0, microsecond=0)
        super().save(*args, **kwargs)
