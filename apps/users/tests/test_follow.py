from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from apps.users.models import Follow


class FollowTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='u1', password='pass')
        self.user2 = User.objects.create_user(username='u2', password='pass')

    def test_follow_and_unfollow_user(self):
        self.client.login(username='u1', password='pass')
        url = reverse('toggle_follow', args=['user', self.user2.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        ct = ContentType.objects.get_for_model(User)
        self.assertTrue(Follow.objects.filter(
            follower_content_type=ct,
            follower_object_id=self.user1.id,
            followed_content_type=ct,
            followed_object_id=self.user2.id
        ).exists())
        response = self.client.post(url)
        self.assertFalse(Follow.objects.filter(
            follower_content_type=ct,
            follower_object_id=self.user1.id,
            followed_content_type=ct,
            followed_object_id=self.user2.id
        ).exists())
