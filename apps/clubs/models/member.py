from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
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
    GUARDIA_CHOICES = [
        ("diestro", "Diestro"),
        ("zurdo", "Zurdo"),
        ("ambidiestro", "Ambidiestro"),
    ]


    FUENTE_CHOICES = [
        ("directa", "Directa"),
        ("presencial", "Presencial"),
        ("telefono", "Telefono"),
        ("otros", "Otros"),
    ]

    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="miembros")
    avatar = models.ImageField(upload_to="miembros/", blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    region = models.CharField(max_length=100, blank=True)
    localidad = models.CharField(max_length=100, blank=True)
    street = models.CharField(max_length=255, blank=True)
    number = models.CharField(max_length=10, blank=True)
    door = models.CharField(max_length=10, blank=True)
    codigo_postal = models.CharField(max_length=10, blank=True)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, blank=True)
    guardia = models.CharField(max_length=11, choices=GUARDIA_CHOICES, blank=True)
    peso = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
    )
    altura = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
    )
    nacionalidad = models.CharField(
        max_length=100,
        blank=True,
        default='España',
    )
    notas = models.TextField(blank=True)
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=150)
    prefijo = models.CharField(max_length=5, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    codigo = models.CharField(max_length=7, unique=True, editable=False, blank=True, null=True)
    fuente = models.CharField(max_length=20, choices=FUENTE_CHOICES, blank=True)
    fecha_inscripcion = models.DateField(auto_now_add=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, blank=True, null=True)

    class Meta:
        verbose_name = "Miembro"
        verbose_name_plural = "Miembros"
        ordering = ["-fecha_inscripcion"]

    def __str__(self):  # pragma: no cover - simple representation
        return f"{self.nombre} {self.apellidos}"

    def save(self, *args, **kwargs):
        if not self.codigo:
            last_codigo = Miembro.objects.aggregate(models.Max('codigo'))['codigo__max']
            if last_codigo:
                try:
                    last_num = int(last_codigo.split('-')[1])
                except (IndexError, ValueError):
                    last_num = 0
            else:
                last_num = 0
            self.codigo = f"B-{last_num + 1:04d}"
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
