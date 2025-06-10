import io
import tempfile
from PIL import Image
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings

from apps.users.models import Profile


class AvatarResizeTests(TestCase):
    def test_avatar_resized_on_save(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with override_settings(MEDIA_ROOT=tmpdir):
                user = User.objects.create_user(username="u", password="pass")
                img = Image.new("RGB", (1000, 1000), "white")
                buf = io.BytesIO()
                img.save(buf, format="JPEG")
                buf.seek(0)
                upload = SimpleUploadedFile("test.jpg", buf.getvalue(), content_type="image/jpeg")
                profile = Profile.objects.create(user=user, avatar=upload)
                width, height = Image.open(profile.avatar.path).size
                self.assertLessEqual(width, 800)
                self.assertLessEqual(height, 800)

