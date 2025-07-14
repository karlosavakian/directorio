from django.db import models
from .club import Club


class Miembro(models.Model):
    ESTADO_CHOICES = [
        ("activo", "Activo"),
        ("inactivo", "Inactivo"),
    ]

    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="miembros")
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=150)
    telefono = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    fecha_inscripcion = models.DateField(auto_now_add=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default="activo")

    class Meta:
        verbose_name = "Miembro"
        verbose_name_plural = "Miembros"
        ordering = ["-fecha_inscripcion"]

    def __str__(self):  # pragma: no cover - simple representation
        return f"{self.nombre} {self.apellidos}"
