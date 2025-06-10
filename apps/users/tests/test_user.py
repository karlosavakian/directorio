from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from unittest.mock import patch


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

        self.assertTrue(User.objects.filter(username="newuser").exists())
        self.assertRedirects(response, reverse("home"))

    def test_welcome_email_sent(self):
        data = {
            "username": "emailuser",
            "email": "email@example.com",
            "password1": "secretpass123",
            "password2": "secretpass123",
        }
        url = reverse("register")
        with patch("apps.users.views.auth.send_welcome_email") as mock_send:
            self.client.post(url, data)
            mock_send.assert_called_once_with("email@example.com")

