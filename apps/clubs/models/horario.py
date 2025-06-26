from django.db import models
from django.utils.translation import gettext_lazy as _
from .club import Club


class Horario(models.Model):
    class Estado(models.TextChoices):
        ABIERTO = "abierto", _("Abierto")
        CERRADO = "cerrado", _("Cerrado")

    class DiasSemana(models.TextChoices):
        LUNES = "lunes", _("Lunes")
        MARTES = "martes", _("Martes")
        MIERCOLES = "miercoles", _("Miércoles")
        JUEVES = "jueves", _("Jueves")
        VIERNES = "viernes", _("Viernes")
        SABADO = "sabado", _("Sábado")
        DOMINGO = "domingo", _("Domingo")

    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="horarios")
    dia = models.CharField(max_length=10, choices=DiasSemana.choices)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    descripcion = models.CharField(max_length=30, blank=True)
    estado = models.CharField(max_length=8, choices=Estado.choices)

    class Meta:
        ordering = ["dia", "hora_inicio"]
        constraints = [
            models.UniqueConstraint(
                fields=["club", "dia"], name="unique_horario_por_dia"
            )
        ]

    def __str__(self):
        return f"{self.club.name} - {self.get_dia_display()} {self.hora_inicio} - {self.hora_fin}"
