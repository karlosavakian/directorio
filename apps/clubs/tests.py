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

    def test_pagination_limits_results(self):
        """Only 12 results should appear on the first page."""
        for i in range(13):
            Club.objects.create(
                name=f"Extra Club {i}",
                city="NY",
                address="addr",
                phone="123",
                email=f"{i}@ex.com",
            )

        url = reverse("search_results")
        response = self.client.get(url, {"q": "Club", "page": 1})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["clubs"]), 12)

    def test_second_page_contains_remaining_results(self):
        for i in range(13):
            Club.objects.create(
                name=f"Another Club {i}",
                city="NY",
                address="addr",
                phone="123",
                email=f"{i}@ex2.com",
            )

        url = reverse("search_results")
        response = self.client.get(url, {"q": "Club", "page": 2})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["clubs"]), 1)
