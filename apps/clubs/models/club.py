from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.db.models import Avg, Count
from django.utils.translation import gettext_lazy as _

from apps.core.utils.image_utils import resize_image

 
class Club(models.Model):
    logo = models.ImageField(upload_to='clubs/logos/', blank=True, null=True)
    owner = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='owned_clubs')
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
    verified = models.BooleanField(default=False)
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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image and hasattr(self.image, 'path'):
            resize_image(self.image.path)

 

