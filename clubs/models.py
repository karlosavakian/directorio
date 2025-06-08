from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User 
from django.db.models import Avg, Count 
from django.utils.translation import gettext_lazy as _

 
class Club(models.Model):
    logo = models.ImageField(upload_to='clubs/logos/', blank=True, null=True)
    name = models.CharField(max_length=255)
    about = models.TextField(blank=True)   
    slug = models.SlugField(unique=True, blank=True)
    city = models.CharField(max_length=100) 
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    whatsapp_link = models.URLField(blank=True, null=True)
    email = models.EmailField()
    features = models.ManyToManyField('Feature', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    CATEGORY_CHOICES = [
        ('club', 'Club'),
        ('entrenador', 'Entrenador'),
        ('manager', 'Manager'),
        ('servicio', 'Servicio'),
    ]
 
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='club'
    )


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    def get_detailed_ratings(self):
        return self.reseñas.aggregate(
            instalaciones=Avg('instalaciones'),
            entrenadores=Avg('entrenadores'),
            ambiente=Avg('ambiente'),
            calidad_precio=Avg('calidad_precio'),
            variedad_clases=Avg('variedad_clases'),
        )
    get_detailed_ratings = get_detailed_ratings

    def average_rating(self):
        result = self.reseñas.aggregate(avg=Avg(
            (models.F('instalaciones') + models.F('entrenadores') +
             models.F('ambiente') + models.F('calidad_precio') +
             models.F('variedad_clases')) / 5
        ))
        return round(result['avg'], 1) if result['avg'] else None

    def reviews_count(self):
        return self.reseñas.count()

class ClubPhoto(models.Model):
    club = models.ForeignKey('Club', related_name='photos', on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='club_photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Foto de {self.club.name if self.club else 'Sin club'}"


class Feature(models.Model):
    name = models.CharField(max_length=100)
    icon = models.FileField(upload_to='features/', blank=True, null=True)

    def __str__(self):
        return self.name

class Clase(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='clases')
    nombre = models.CharField(max_length=100)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    def __str__(self):
        return f"{self.nombre} ({self.hora_inicio} - {self.hora_fin})"

class Competidor(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='competidores')
    nombre = models.CharField(max_length=100)
    victorias = models.IntegerField(default=0)
    derrotas = models.IntegerField(default=0)
    empates = models.IntegerField(default=0)
    titulos = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

VALORACION_CHOICES = [(i, str(i)) for i in range(1, 6)]

class Reseña(models.Model):
    club = models.ForeignKey('Club', on_delete=models.CASCADE, related_name='reseñas')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    instalaciones = models.PositiveIntegerField(choices=VALORACION_CHOICES)
    entrenadores = models.PositiveIntegerField(choices=VALORACION_CHOICES)
    ambiente = models.PositiveIntegerField(choices=VALORACION_CHOICES)
    calidad_precio = models.PositiveIntegerField(choices=VALORACION_CHOICES)
    variedad_clases = models.PositiveIntegerField(choices=VALORACION_CHOICES)
    
    comentario = models.TextField(blank=True)
    creado = models.DateTimeField(auto_now_add=True)

    def promedio(self):
        return round((
            self.instalaciones + self.entrenadores +
            self.ambiente + self.calidad_precio + self.variedad_clases
        ) / 5, 1)

    def __str__(self):
        return f"{self.usuario.username} - {self.club.name} ({self.promedio()}⭐)"
    @property
    def average_rating(self):
        reseñas = self.reseñas.all()
        if not reseñas.exists():
            return None
        total = sum([r.promedio() for r in reseñas])
        return round(total / reseñas.count(), 1)

    @property
    def reviews_count(self):
        return self.reseñas.count()
    
    
class Horario(models.Model):
    class DiasSemana(models.TextChoices):
        LUNES = 'lunes', _('Lunes')
        MARTES = 'martes', _('Martes')
        MIERCOLES = 'miercoles', _('Miércoles')
        JUEVES = 'jueves', _('Jueves')
        VIERNES = 'viernes', _('Viernes')
        SABADO = 'sabado', _('Sábado')
        DOMINGO = 'domingo', _('Domingo')

    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='horarios')
    dia = models.CharField(max_length=10, choices=DiasSemana.choices)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    class Meta:
        ordering = ['dia', 'hora_inicio']

    def __str__(self):
        return f"{self.club.name} - {self.get_dia_display()} {self.hora_inicio} - {self.hora_fin}"