# apps/core/models.py
from django.db import models

class TimeStampedModel(models.Model):
    """ Modelo base que agrega timestamps a cualquier modelo que lo extienda """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
