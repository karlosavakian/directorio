from django.test import TestCase
from django.urls import reverse

from .models import Club


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