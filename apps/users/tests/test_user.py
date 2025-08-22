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
            "password1": "Secretpass123",
            "password2": "Secretpass123",
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
            "password1": "Secretpass123",
            "password2": "Secretpass123",
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
            "password1": "Secretpass123",
            "password2": "Secretpass123",
        }
        url = reverse("register")
        with patch("apps.users.views.auth.send_welcome_email") as mock_send:
            self.client.post(url, data)
            mock_send.assert_called_once_with("email@example.com")

    def test_username_too_short(self):
        data = {
            "username": "ab",
            "email": "short@example.com",
            "password1": "Secretpass123",
            "password2": "Secretpass123",
        }
        url = reverse("register")
        response = self.client.post(url, data)
        self.assertContains(response, "El nombre de usuario debe tener al menos 3 caracteres")
        self.assertFalse(User.objects.filter(username="ab").exists())

    def test_disposable_email_rejected(self):
        data = {
            "username": "tempuser",
            "email": "temp@yopmail.com",
            "password1": "Secretpass123",
            "password2": "Secretpass123",
        }
        url = reverse("register")
        response = self.client.post(url, data)
        self.assertContains(response, "Introduzca un correo electrónico valido, el dominio usado no está permitido.")
        self.assertFalse(User.objects.filter(username="tempuser").exists())

    def test_password_requirements(self):
        data = {
            "username": "weakpass",
            "email": "weak@example.com",
            "password1": "weak",
            "password2": "weak",
        }
        url = reverse("register")
        response = self.client.post(url, data)
        self.assertContains(
            response,
            "La contraseña debe tener al menos 6 caracteres e incluir mayúsculas, minúsculas y números.",
        )
        self.assertFalse(User.objects.filter(username="weakpass").exists())


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


class ProfileEmailTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="profileupdate", email="old@example.com", password="pass"
        )

    def test_disposable_email_rejected_on_update(self):
        self.client.login(username="profileupdate", password="pass")
        url = reverse("profile")
        data = {"username": "profileupdate", "email": "temp@yopmail.com"}
        response = self.client.post(url, data)
        self.assertContains(
            response,
            "Introduzca un correo electrónico valido, el dominio usado no está permitido.",
        )
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "old@example.com")


class ProfilePasswordTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="passuser", email="pass@example.com", password="oldpass123"
        )
        self.client.login(username="passuser", password="oldpass123")
        self.url = reverse("profile")

    def test_short_password_rejected(self):
        data = {
            "username": "passuser",
            "new_password1": "short",
            "new_password2": "short",
        }
        response = self.client.post(self.url, data)
        self.assertContains(
            response,
            "La contraseña debe tener al menos 6 caracteres e incluir mayúsculas, minúsculas y números.",
        )
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("oldpass123"))

    def test_redirects_to_previous_page_after_password_change(self):
        data = {
            "username": "passuser",
            "new_password1": "StrongPass123",
            "new_password2": "StrongPass123",
        }
        response = self.client.post(self.url, data, HTTP_REFERER="/prev/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/prev/")
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("StrongPass123"))

