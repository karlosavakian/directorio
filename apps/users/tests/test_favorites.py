from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from apps.clubs.models import Club
from apps.users.models import Follow


class FavoritesViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='u', password='pass')
        self.club = Club.objects.create(
            name='Club Favorito',
            city='City',
            address='Address',
            phone='123',
            email='c@example.com'
        )
        follower_ct = ContentType.objects.get_for_model(self.user)
        club_ct = ContentType.objects.get_for_model(Club)
        Follow.objects.create(
            follower_content_type=follower_ct,
            follower_object_id=self.user.id,
            followed_content_type=club_ct,
            followed_object_id=self.club.id,
        )

    def test_clubs_followed_are_listed(self):
        self.client.login(username='u', password='pass')
        url = reverse('favoritos')
        response = self.client.get(url)
        self.assertContains(response, 'Club Favorito')

