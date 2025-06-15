from django.db import models


class ClubPost(models.Model):
    club = models.ForeignKey('Club', on_delete=models.CASCADE, related_name='posts')
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    evento_fecha = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.titulo} - {self.club.name}"
