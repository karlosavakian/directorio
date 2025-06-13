import io
import tempfile
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings

from apps.users.forms import ProfileForm

class AvatarValidationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="u", password="pass")
        self.profile = self.user.profile

    def test_avatar_size_limit(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with override_settings(MEDIA_ROOT=tmpdir):
                big_content = b"a" * (2 * 1024 * 1024 + 1)
                upload = SimpleUploadedFile("big.jpg", big_content, content_type="image/jpeg")
                form = ProfileForm(data={}, files={"avatar": upload}, instance=self.profile)
                self.assertFalse(form.is_valid())
                self.assertIn("2MB", form.errors["avatar"][0])

    def test_avatar_format_validation(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with override_settings(MEDIA_ROOT=tmpdir):
                upload = SimpleUploadedFile("test.gif", b"GIF89a", content_type="image/gif")
                form = ProfileForm(data={}, files={"avatar": upload}, instance=self.profile)
                self.assertFalse(form.is_valid())
                self.assertIn("JPG", form.errors["avatar"][0])
