from django.db import models
from django.contrib.auth.models import User

from apps.core.utils.image_utils import resize_image


class ClubPost(models.Model):
    club = models.ForeignKey('Club', on_delete=models.CASCADE, related_name='posts')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='club_posts')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    titulo = models.CharField(max_length=200, blank=True)
    contenido = models.TextField()
    image = models.ImageField(upload_to='club_post_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    evento_fecha = models.DateField(blank=True, null=True)
    likes = models.ManyToManyField(
        User,
        related_name="liked_clubposts",
        blank=True,
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.titulo} - {self.club.name}"

    @property
    def is_root(self):
        return self.parent is None

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image and hasattr(self.image, 'path'):
            resize_image(self.image.path)
