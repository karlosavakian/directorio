from django.db import models
 
class Feature(models.Model):
    name = models.CharField(max_length=100)
    icon = models.FileField(upload_to='features/', blank=True, null=True)

    def __str__(self):
        return self.name