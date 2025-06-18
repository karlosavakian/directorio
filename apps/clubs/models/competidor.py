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
    record = models.CharField(max_length=20, blank=True)
    modalidad = models.CharField(max_length=15, choices=MODALIDAD_CHOICES, blank=True)
    peso = models.CharField(max_length=15, choices=PESO_CHOICES, blank=True)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, blank=True)
    palmares = models.TextField(blank=True, verbose_name="Palmarés")

    def save(self, *args, **kwargs):
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
        return self.nombre

    @property
    def record_tuple(self):
        """Return wins, losses and draws as integers."""
        try:
            wins, losses, draws = [int(p) for p in self.record.split("-")]
            return wins, losses, draws
        except Exception:
            return 0, 0, 0
