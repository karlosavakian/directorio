from datetime import date

from django.db import models
from .club import Club
from apps.core.utils.image_utils import resize_image


class Competidor(models.Model):
    MODALIDAD_CHOICES = [
        ("elite", "Elite"),
        ("joven", "Joven"),
        ("junior", "Junior"),
        ("schoolboy", "Schoolboy"),
        ("profesional", "Profesional"),
    ]

    PESO_CHOICES = [
        ("minimosca", "Minimosca"),
        ("mosca", "Mosca"),
        ("gallo", "Gallo"),
        ("pluma", "Pluma"),
        ("ligero", "Ligero"),
        ("welter", "Wélter"),
        ("superwelter", "Superwélter"),
        ("medio", "Medio"),
        ("semipesado", "Semipesado"),
        ("crucero", "Crucero"),
        ("pesado", "Pesado"),
        ("superpesado", "Superpesado"),
    ]

    SEXO_CHOICES = [
        ("M", "Masculino"),
        ("F", "Femenino"),
    ]

    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="competidores")
    avatar = models.ImageField(upload_to="competidores/", blank=True, null=True)
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=150, blank=True)
    edad = models.PositiveIntegerField(null=True, blank=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    record = models.CharField(max_length=20, blank=True)
    modalidad = models.CharField(max_length=15, choices=MODALIDAD_CHOICES, blank=True)
    peso = models.CharField(max_length=15, choices=PESO_CHOICES, blank=True)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, blank=True)
    peso_kg = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    altura_cm = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    palmares = models.TextField(blank=True, verbose_name="Palmarés")

    def save(self, *args, **kwargs):
        if self.fecha_nacimiento:
            today = date.today()
            self.edad = (
                today.year
                - self.fecha_nacimiento.year
                - ((today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day))
            )

        if self.edad is not None and not self.modalidad:
            if 13 <= self.edad <= 14:
                self.modalidad = "schoolboy"
            elif 15 <= self.edad <= 16:
                self.modalidad = "junior"
            elif 17 <= self.edad <= 18:
                self.modalidad = "joven"
            elif 19 <= self.edad <= 40:
                self.modalidad = "elite"
            elif self.edad >= 18:
                self.modalidad = "profesional"
        super().save(*args, **kwargs)
        if self.avatar and hasattr(self.avatar, "path"):
            resize_image(self.avatar.path)

    @property
    def categoria(self):
        parts = []
        if self.modalidad:
            parts.append(self.get_modalidad_display())
        if self.peso:
            parts.append(self.get_peso_display())
        if self.sexo:
            parts.append(self.get_sexo_display())
        return " ".join(parts)

    def __str__(self):
        return f"{self.nombre} {self.apellidos}".strip()

    @property
    def record_tuple(self):
        """Return wins, losses and draws as integers."""
        try:
            wins, losses, draws = [int(p) for p in self.record.split("-")]
            return wins, losses, draws
        except Exception:
            return 0, 0, 0
