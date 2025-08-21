from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class ProfileUsernameUpdateTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='olduser', password='pass')

    def test_username_updates_on_profile_save(self):
        self.client.login(username='olduser', password='pass')
        url = reverse('profile')
        response = self.client.post(url, {'username': 'newuser'})
        self.assertRedirects(response, url)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'newuser')

