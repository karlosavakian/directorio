from django.db import models
from .horario import Horario


class ClaseHorario(models.Model):
    """Rango horario asociado a un día concreto."""
    horario = models.ForeignKey(Horario, related_name="clases", on_delete=models.CASCADE)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    descripcion = models.CharField(max_length=20, blank=True)

    class Meta:
        ordering = ["hora_inicio"]

    def __str__(self) -> str:  # pragma: no cover - simple representation
        if self.descripcion:
            return f"{self.hora_inicio} - {self.hora_fin} ({self.descripcion})"
        return f"{self.hora_inicio} - {self.hora_fin}"
