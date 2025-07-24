from django.db import models

class BookingClass(models.Model):
    club = models.ForeignKey('Club', on_delete=models.CASCADE, related_name='booking_classes')
    titulo = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    duracion = models.PositiveIntegerField(help_text='Duración en minutos')
    detalle = models.CharField(max_length=400, blank=True)
    destacado = models.BooleanField(default=False)

    class Meta:
        ordering = ['-destacado', 'titulo']

    def __str__(self):
        return self.titulo
