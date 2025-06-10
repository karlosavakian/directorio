from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Follow(models.Model):
    follower_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name="follow_follower")
    follower_object_id = models.PositiveIntegerField()
    follower = GenericForeignKey('follower_content_type', 'follower_object_id')

    followed_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name="follow_followed")
    followed_object_id = models.PositiveIntegerField()
    followed = GenericForeignKey('followed_content_type', 'followed_object_id')

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            'follower_content_type', 'follower_object_id',
            'followed_content_type', 'followed_object_id'
        )

    def __str__(self):
        return f"{self.follower} sigue a {self.followed}"
