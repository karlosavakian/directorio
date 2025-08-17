from django.contrib.auth.models import User
from django.db import models

from apps.core.utils.image_utils import resize_image

PLAN_CHOICES = [
    ("bronce", "Plan Bronce"),
    ("plata", "Plan Plata"),
    ("oro", "Plan Oro"),
]


PROFILE_TYPE_CHOICES = [
    ("club_owner", "Club Owner"),
    ("coach", "Coach"),
]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    notifications = models.BooleanField(default=True)
    plan = models.CharField(max_length=10, choices=PLAN_CHOICES, default="bronce")
    profile_type = models.CharField(
        max_length=20,
        choices=PROFILE_TYPE_CHOICES,
        default="club_owner",
    )

    def __str__(self):
        return f"Perfil de {self.user.username}"

    def save(self, *args, **kwargs):
        # When a Profile is automatically created via signals, calling
        # ``Profile.objects.create`` again for the same user would raise
        # an ``IntegrityError`` because of the ``OneToOneField``. To make
        # avatar uploads more robust, detect this situation and update the
        # existing profile instead of attempting a second insert.
        if not self.pk:
            existing = Profile.objects.filter(user=self.user).first()
            if existing:
                self.pk = existing.pk
                # ``Model.save(force_insert=True)`` is used by ``objects.create``.
                # Remove the flag so we update the existing row instead.
                kwargs.pop("force_insert", None)

        super().save(*args, **kwargs)
        if self.avatar and hasattr(self.avatar, "path"):
            resize_image(self.avatar.path)
