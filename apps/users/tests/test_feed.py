from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from apps.clubs.models import Club, ClubPost, Reseña
from apps.users.models import Follow

class FeedViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='follower', password='pass')
        self.poster = User.objects.create_user(username='poster', password='pass')
        self.club = Club.objects.create(name='Club', city='C', address='A', phone='1', email='e@e.com')
        self.post = ClubPost.objects.create(club=self.club, user=self.poster, titulo='t', contenido='club post')
        self.review = Reseña.objects.create(club=self.club, usuario=self.poster, titulo='r', comentario='club review', instalaciones=1, entrenadores=1, ambiente=1, calidad_precio=1, variedad_clases=1)

    def test_feed_shows_followed_club_posts(self):
        self.client.login(username='follower', password='pass')
        url = reverse('toggle_follow', args=['club', self.club.id])
        self.client.post(url)

        response = self.client.get(reverse('feed'))

        self.assertContains(response, 'club post')
        self.assertContains(response, 'club review')

