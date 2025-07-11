from django.db import models
from .resena import Reseña
from apps.core.utils.image_utils import resize_image

class ReseñaPhoto(models.Model):
    reseña = models.ForeignKey(Reseña, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='review_photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Foto reseña {self.reseña_id}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image and hasattr(self.image, 'path'):
            resize_image(self.image.path)

