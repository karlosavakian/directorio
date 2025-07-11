from django.db import models
from django.utils.text import slugify
from apps.core.models import TimeStampedModel


class BlogPost(TimeStampedModel):
    """Simple blog post to be displayed on the /blog page."""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
