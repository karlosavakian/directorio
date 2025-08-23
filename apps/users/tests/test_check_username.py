from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class CheckUsernameTests(TestCase):
    def setUp(self):
        self.url = reverse('check_username')
        self.user = User.objects.create_user(username='existing', password='pass')

    def test_available_for_new_username(self):
        response = self.client.get(self.url, {'username': 'unique'})
        self.assertEqual(response.json(), {'available': True})

    def test_unavailable_for_taken_username(self):
        response = self.client.get(self.url, {'username': 'existing'})
        self.assertEqual(response.json(), {'available': False})

    def test_current_user_username_is_available(self):
        self.client.login(username='existing', password='pass')
        response = self.client.get(self.url, {'username': 'existing'})
        self.assertEqual(response.json(), {'available': True})
