from django.db import models
from django.contrib.auth.models import User


class ClubPost(models.Model):
    club = models.ForeignKey('Club', on_delete=models.CASCADE, related_name='posts')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='club_posts')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    titulo = models.CharField(max_length=200, blank=True)
    contenido = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    evento_fecha = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.titulo} - {self.club.name}"

    @property
    def is_root(self):
        return self.parent is None
