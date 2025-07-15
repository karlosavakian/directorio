from django.db import models
from django.utils import timezone
from .club import Club
from apps.core.utils.image_utils import resize_image


class Miembro(models.Model):
    ESTADO_CHOICES = [
        ("activo", "Activo"),
        ("inactivo", "Inactivo"),
    ]

    SEXO_CHOICES = [
        ("M", "Masculino"),
        ("F", "Femenino"),
    ]

    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="miembros")
    avatar = models.ImageField(upload_to="miembros/", blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, blank=True)
    peso = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    altura = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    nacionalidad = models.CharField(max_length=100, blank=True)
    notas = models.TextField(blank=True)
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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.avatar and hasattr(self.avatar, "path"):
            resize_image(self.avatar.path)

    @property
    def pago_mes_actual(self):
        """Return 'completo' if there's a payment for the current month."""
        today = timezone.now().date()
        has_payment = self.pagos.filter(
            fecha__year=today.year, fecha__month=today.month
        ).exists()
        return "completo" if has_payment else "pendiente"
