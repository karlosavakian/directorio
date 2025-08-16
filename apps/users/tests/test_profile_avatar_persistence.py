import io
import tempfile
from PIL import Image
from django.contrib.auth.models import User
from apps.clubs.models import Club
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
                self.assertContains(response, self.user.profile.avatar.url)
                self.assertContains(response, 'class="nav-avatar-img"')

    @override_settings(ALLOWED_HOSTS=["testserver"])
    def test_nav_avatar_on_owned_club_profile(self):
        """Nav avatar should use the uploaded profile image on owned club pages."""
        self.client.login(username="avataruser", password="pass")
        with tempfile.TemporaryDirectory() as tmpdir:
            with override_settings(MEDIA_ROOT=tmpdir):
                # Create a club with a logo to ensure nav avatar prefers the
                # user's profile avatar over the club logo.
                img_logo = Image.new("RGB", (50, 50), "white")
                buf_logo = io.BytesIO()
                img_logo.save(buf_logo, format="JPEG")
                buf_logo.seek(0)
                logo_upload = SimpleUploadedFile("logo.jpg", buf_logo.getvalue(), content_type="image/jpeg")
                club = Club.objects.create(
                    name="Club Avatar",
                    city="C",
                    address="A",
                    phone="1",
                    email="e@e.com",
                    owner=self.user,
                    logo=logo_upload,
                )

                # Upload a profile avatar for the user.
                img = Image.new("RGB", (50, 50), "white")
                buf = io.BytesIO()
                img.save(buf, format="JPEG")
                buf.seek(0)
                upload = SimpleUploadedFile("avatar.jpg", buf.getvalue(), content_type="image/jpeg")
                self.client.post(
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
                response = self.client.get(reverse("club_profile", args=[club.slug]))
                self.assertContains(response, self.user.profile.avatar.url)
                self.assertContains(response, 'class="nav-avatar-img"')

    @override_settings(ALLOWED_HOSTS=["testserver"])
    def test_header_displays_initial_when_no_avatar(self):
        """Header should show the first letter of username when no avatar exists."""
        self.client.login(username="avataruser", password="pass")
        response = self.client.get(reverse("profile"))
        html = response.content.decode()
        expected_div = f'<div class="nav-avatar">{self.user.username[0].upper()}</div>'
        self.assertInHTML(expected_div, html)
