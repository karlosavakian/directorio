from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

from .club import Club
from apps.core.utils.image_utils import resize_image


class TrainingLevel(models.Model):
    """Modelo simple para los niveles que puede impartir un entrenador."""
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Nivel"
        verbose_name_plural = "Niveles"

    def __str__(self) -> str:  # pragma: no cover - simple representation
        return self.name

class Entrenador(models.Model):
    CITY_CHOICES = [
        ("Madrid", "Madrid"),
        ("Barcelona", "Barcelona"),
        ("Valencia", "Valencia"),
        ("Sevilla", "Sevilla"),
        ("Zaragoza", "Zaragoza"),
    ]

    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='entrenadores')
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='coach_profile',
        null=True,
        blank=True,
    )
    avatar = models.ImageField(upload_to='entrenadores/', blank=True, null=True)
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, blank=True, null=True)
    ciudad = models.CharField(max_length=50, choices=CITY_CHOICES, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    whatsapp = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    verificado = models.BooleanField(default=False)
    niveles = models.ManyToManyField(TrainingLevel, blank=True)
    precio_hora = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    promociones = models.TextField(blank=True)
    clase_prueba = models.BooleanField(default=False)
    experiencia_anos = models.PositiveIntegerField(null=True, blank=True)
    bio = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.nombre}-{self.apellidos}")
        super().save(*args, **kwargs)
        if self.avatar and hasattr(self.avatar, "path"):
            resize_image(self.avatar.path)

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"


class EntrenadorPhoto(models.Model):
    """Fotos adicionales asociadas a un entrenador."""
    entrenador = models.ForeignKey(Entrenador, related_name="photos", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="coach_photos/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:  # pragma: no cover - simple representation
        return f"Foto de {self.entrenador}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image and hasattr(self.image, "path"):
            resize_image(self.image.path)
