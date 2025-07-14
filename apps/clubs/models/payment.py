from django.db import models
from .member import Miembro


class Pago(models.Model):
    miembro = models.ForeignKey(Miembro, on_delete=models.CASCADE, related_name="pagos")
    fecha = models.DateField()
    monto = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"
        ordering = ["-fecha"]

    def __str__(self):  # pragma: no cover - simple representation
        return f"{self.miembro} - {self.fecha} - {self.monto}"
