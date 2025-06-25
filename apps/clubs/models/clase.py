from django.db import models
from .horario import Horario


class Clase(models.Model):
    """Clase programada dentro de un horario semanal."""
    horario = models.ForeignKey(Horario, related_name="clases", on_delete=models.CASCADE)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    texto = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["hora_inicio"]

    def __str__(self) -> str:  # pragma: no cover - simple representation
        if self.texto:
            return f"{self.hora_inicio} - {self.hora_fin} ({self.texto})"
        return f"{self.hora_inicio} - {self.hora_fin}"
