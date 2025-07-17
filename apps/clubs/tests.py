import io
import tempfile
from django.test import TestCase, override_settings
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User, Group
from PIL import Image

from .models import Club, ClubPhoto, ClubPost, Miembro, Pago
from datetime import date


class SearchResultsTests(TestCase):
    """Tests for the ``search_results`` view."""

    def setUp(self):
        self.club = Club.objects.create(
            name="Boxing Club",
            city="New York",
            address="1 Main St",
            phone="1234567",
            email="club@example.com",
        )

    def test_search_returns_results(self):
        """The view should return the club matching the query."""
        url = reverse("search_results")
        response = self.client.get(url, {"q": "Box"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.club.name)

    def test_pagination_limits_results(self):
        """Only 12 results should appear on the first page."""
        for i in range(13):
            Club.objects.create(
                name=f"Extra Club {i}",
                city="NY",
                address="addr",
                phone="123",
                email=f"{i}@ex.com",
            )

        url = reverse("search_results")
        response = self.client.get(url, {"q": "Club", "page": 1})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["clubs"]), 12)

    def test_second_page_contains_remaining_results(self):
        for i in range(13):
            Club.objects.create(
                name=f"Another Club {i}",
                city="NY",
                address="addr",
                phone="123",
                email=f"{i}@ex2.com",
            )

        url = reverse("search_results")
        response = self.client.get(url, {"q": "Club", "page": 2})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["clubs"]), 1)

class ClubPhotoResizeTests(TestCase):
    def test_photo_resized_on_save(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with override_settings(MEDIA_ROOT=tmpdir):
                club = Club.objects.create(
                    name="Club",
                    city="City",
                    address="Add",
                    phone="1",
                    email="c@example.com",
                )
                img = Image.new("RGB", (1000, 1000), "white")
                buf = io.BytesIO()
                img.save(buf, format="JPEG")
                buf.seek(0)
                upload = SimpleUploadedFile("test.jpg", buf.getvalue(), content_type="image/jpeg")
                photo = ClubPhoto.objects.create(club=club, image=upload)
                width, height = Image.open(photo.image.path).size
                self.assertLessEqual(width, 800)
        self.assertLessEqual(height, 800)


class DashboardPermissionTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username='owner', password='pass')
        self.other = User.objects.create_user(username='other', password='pass')
        self.club = Club.objects.create(
            name='Owner Club',
            city='C',
            address='A',
            phone='1',
            email='e@example.com',
            owner=self.owner,
        )
        Group.objects.get_or_create(name='ClubOwner')

    def test_non_owner_cannot_edit_club(self):
        self.client.login(username='other', password='pass')
        url = reverse('club_edit', args=[self.club.slug])
        response = self.client.post(url, {'name': 'X'})
        self.assertEqual(response.status_code, 403)

    def test_non_owner_cannot_edit_post(self):
        post = ClubPost.objects.create(club=self.club, user=self.owner, titulo='t', contenido='c')
        self.client.login(username='other', password='pass')
        url = reverse('clubpost_update', args=[post.pk])
        response = self.client.post(url, {'titulo': 'x', 'contenido': 'y'})
        self.assertEqual(response.status_code, 403)

    def test_non_owner_cannot_create_post(self):
        self.client.login(username='other', password='pass')
        url = reverse('clubpost_create', args=[self.club.slug])
        response = self.client.post(url, {'titulo': 'x', 'contenido': 'y'})
        self.assertEqual(response.status_code, 403)


class UserReviewFirstTests(TestCase):
    def setUp(self):
        self.club = Club.objects.create(
            name='My Club',
            city='City',
            address='Addr',
            phone='111',
            email='club@example.com',
        )
        self.user1 = User.objects.create_user(username='user1', password='pass')
        self.user2 = User.objects.create_user(username='user2', password='pass')

        self.review1 = Reseña.objects.create(
            club=self.club,
            usuario=self.user1,
            titulo='U1',
            instalaciones=5,
            entrenadores=5,
            ambiente=5,
            calidad_precio=5,
            variedad_clases=5,
            comentario='great',
        )
        self.review2 = Reseña.objects.create(
            club=self.club,
            usuario=self.user2,
            titulo='U2',
            instalaciones=4,
            entrenadores=4,
            ambiente=4,
            calidad_precio=4,
            variedad_clases=4,
            comentario='ok',
        )

    def test_user_review_first_in_profile(self):
        self.client.login(username='user1', password='pass')
        url = reverse('club_profile', args=[self.club.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        reviews = list(response.context['reseñas'])
        self.assertEqual(reviews[0].usuario, self.user1)

    def test_user_review_first_in_ajax(self):
        self.client.login(username='user1', password='pass')
        url = reverse('ajax_reviews', args=[self.club.slug])
        response = self.client.get(url, {'orden': 'recientes'}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        reviews = list(response.context['reseñas'])
        self.assertEqual(reviews[0].usuario, self.user1)


class DashboardMemberFilterTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username='owner', password='pass')
        Group.objects.get_or_create(name='ClubOwner')
        self.club = Club.objects.create(
            name='Club', city='C', address='A', phone='1', email='e@e.com', owner=self.owner
        )
        self.member1 = Miembro.objects.create(
            club=self.club, nombre='Ana', apellidos='A', estado='activo', sexo='F'
        )
        self.member2 = Miembro.objects.create(
            club=self.club, nombre='Luis', apellidos='B', estado='inactivo', sexo='M'
        )
        Pago.objects.create(miembro=self.member1, fecha=date.today(), monto=10)
        self.client.login(username='owner', password='pass')

    def test_filter_by_estado(self):
        url = reverse('club_dashboard', args=[self.club.slug])
        res = self.client.get(url, {'estado': 'activo'})
        self.assertContains(res, 'Ana')
        self.assertNotContains(res, 'Luis')

    def test_filter_by_pago(self):
        url = reverse('club_dashboard', args=[self.club.slug])
        res = self.client.get(url, {'pago': 'completo'})
        self.assertContains(res, 'Ana')
        self.assertNotContains(res, 'Luis')

    def test_order_alpha(self):
        url = reverse('club_dashboard', args=[self.club.slug])
        res = self.client.get(url, {'orden': 'alpha'})
        members = list(res.context['members'])
        self.assertEqual(members[0], self.member1)
