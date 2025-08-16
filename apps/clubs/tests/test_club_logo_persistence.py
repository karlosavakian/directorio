import io
import tempfile
from PIL import Image
from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from apps.clubs.models import Club, Feature


class ClubLogoPersistenceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="clublogo", password="pass")

    @override_settings(ALLOWED_HOSTS=["testserver"])
    def test_nav_avatar_updates_with_club_logo(self):
        feature = Feature.objects.create(name="Ring")
        club = Club.objects.create(
            owner=self.user,
            name="Logo Club",
            about="about",
            country="España",
            region="Madrid",
            city="Madrid",
            street="Street",
            number="1",
            postal_code="28001",
            prefijo="+34",
            phone="123456789",
            email="club@example.com",
        )
        club.features.add(feature)
        self.client.login(username="clublogo", password="pass")

        with tempfile.TemporaryDirectory() as tmpdir:
            with override_settings(MEDIA_ROOT=tmpdir):
                img = Image.new("RGB", (50, 50), "white")
                buf = io.BytesIO()
                img.save(buf, format="JPEG")
                buf.seek(0)
                upload = SimpleUploadedFile("logo.jpg", buf.getvalue(), content_type="image/jpeg")
                club.logo.save("logo.jpg", upload)
                club.save()
                response = self.client.get(reverse("club_profile", args=[club.slug]))
                self.assertContains(response, club.logo.url)
                self.assertContains(response, 'class="nav-avatar-img"')

