import io
import tempfile
from django.test import TestCase, override_settings
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image

from .models import Club, ClubPhoto


class SearchResultsTests(TestCase):
    """Tests for the ``search_results`` view."""

    def setUp(self):
        self.club = Club.objects.create(
            name="Boxing Club",
            city="New York",
            address="1 Main St",
            phone="1234567",
            email="club@example.com",
        )

    def test_search_returns_results(self):
        """The view should return the club matching the query."""
        url = reverse("search_results")
        response = self.client.get(url, {"q": "Box"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.club.name)


class ClubPhotoResizeTests(TestCase):
    def test_photo_resized_on_save(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with override_settings(MEDIA_ROOT=tmpdir):
                club = Club.objects.create(
                    name="Club",
                    city="City",
                    address="Add",
                    phone="1",
                    email="c@example.com",
                )
                img = Image.new("RGB", (1000, 1000), "white")
                buf = io.BytesIO()
                img.save(buf, format="JPEG")
                buf.seek(0)
                upload = SimpleUploadedFile("test.jpg", buf.getvalue(), content_type="image/jpeg")
                photo = ClubPhoto.objects.create(club=club, image=upload)
                width, height = Image.open(photo.image.path).size
                self.assertLessEqual(width, 800)
                self.assertLessEqual(height, 800)

