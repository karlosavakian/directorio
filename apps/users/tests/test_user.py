from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from apps.users.models import Profile
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
        user = User.objects.get(username="newuser")
        self.assertFalse(user.profile.notifications)
        # And the view should redirect to home
        self.assertRedirects(response, reverse("home"))

    def test_user_can_opt_in_notifications(self):
        data = {
            "username": "notifyuser",
            "email": "notify@example.com",
            "password1": "secretpass123",
            "password2": "secretpass123",
            "notifications": "on",
        }
        url = reverse("register")
        self.client.post(url, data)

        user = User.objects.get(username="notifyuser")
        self.assertTrue(user.profile.notifications)

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

    def test_username_too_short(self):
        data = {
            "username": "ab",
            "email": "short@example.com",
            "password1": "secretpass123",
            "password2": "secretpass123",
        }
        url = reverse("register")
        response = self.client.post(url, data)
        self.assertContains(response, "El nombre de usuario debe tener al menos 3 caracteres")
        self.assertFalse(User.objects.filter(username="ab").exists())


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

    def test_login_page_includes_labels_and_toggle(self):
        url = reverse("login")
        response = self.client.get(url)
        self.assertContains(response, 'Nombre de usuario o correo electrónico')
        self.assertContains(response, 'Contraseña')
        self.assertContains(response, 'Recordar contraseña')
        self.assertContains(response, 'toggle-password')


class ProfileCreationTests(TestCase):
    def test_profile_created_on_user_creation(self):
        user = User.objects.create_user(username="signaluser", password="pass")
        self.assertTrue(Profile.objects.filter(user=user).exists())

