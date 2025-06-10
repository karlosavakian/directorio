# tests.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class RegistrationTests(TestCase):
    def test_user_can_register(self):
        """Posting valid data should create a user and redirect."""
        data = {
            "username": "newuser",
            "email": "new@example.com",
            "password1": "secretpass123",
            "password2": "secretpass123",
        }
        url = reverse("register")
        response = self.client.post(url, data)

        # A new user should be created
        self.assertTrue(User.objects.filter(username="newuser").exists())
        # And the view should redirect to home
        self.assertRedirects(response, reverse("home"))