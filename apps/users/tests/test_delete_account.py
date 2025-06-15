from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class DeleteAccountTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='deluser', password='pass')

    def test_user_can_delete_account(self):
        self.client.login(username='deluser', password='pass')
        response = self.client.post(reverse('delete_account'))
        self.assertRedirects(response, reverse('home'))
        self.assertFalse(User.objects.filter(username='deluser').exists())
        self.assertNotIn('_auth_user_id', self.client.session)

