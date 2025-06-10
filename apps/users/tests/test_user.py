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


class LoginRememberMeTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="loginuser", password="pass")

    def test_unchecked_remember_me_expires_on_close(self):
        url = reverse("login")
        data = {"username": "loginuser", "password": "pass"}
        self.client.post(url, data)
        self.assertTrue("_auth_user_id" in self.client.session)
        self.assertTrue(self.client.session.get_expire_at_browser_close())

    def test_checked_remember_me_persists_session(self):
        url = reverse("login")
        data = {"username": "loginuser", "password": "pass", "remember_me": "on"}
        self.client.post(url, data)
        self.assertTrue("_auth_user_id" in self.client.session)
        self.assertFalse(self.client.session.get_expire_at_browser_close())


class LoginPageTests(TestCase):
    def test_login_form_shows_username_and_password_fields(self):
        url = reverse("login")
        response = self.client.get(url)
        self.assertContains(response, 'name="username"')
        self.assertContains(response, 'name="password"')

