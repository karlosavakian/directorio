import io
import tempfile
from PIL import Image
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

class ProfileAvatarPersistenceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="avataruser", password="pass")

    @override_settings(ALLOWED_HOSTS=["testserver"])
    def test_avatar_saved_and_header_updated(self):
        self.client.login(username="avataruser", password="pass")
        with tempfile.TemporaryDirectory() as tmpdir:
            with override_settings(MEDIA_ROOT=tmpdir):
                img = Image.new("RGB", (50, 50), "white")
                buf = io.BytesIO()
                img.save(buf, format="JPEG")
                buf.seek(0)
                upload = SimpleUploadedFile("avatar.jpg", buf.getvalue(), content_type="image/jpeg")
                response = self.client.post(
                    reverse("profile"),
                    {
                        "username": "avataruser",
                        "email": "",
                        "new_password1": "",
                        "new_password2": "",
                        "notifications": "on",
                        "avatar": upload,
                    },
                    follow=True,
                )
                self.user.refresh_from_db()
                self.assertEqual(response.status_code, 200)
                self.assertTrue(self.user.profile.avatar.name)
                self.assertContains(response, self.user.profile.avatar.url)

                # nav avatar in header should display the uploaded image
                html = response.content.decode()
                expected_img = (
                    f'<img src="{self.user.profile.avatar.url}" '
                    f'alt="{self.user.username}" class="nav-avatar-img">'
                )
                self.assertInHTML(expected_img, html)
