import io
import tempfile
from django.test import TestCase, override_settings
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User, Group
from PIL import Image

from .models import Club, ClubPhoto, ClubPost, Miembro, Pago, Competidor
from datetime import date


class ClubPlanTests(TestCase):
    def test_default_plan_bronce(self):
        club = Club.objects.create(
            name="Plan Club",
            city="C",
            address="A",
            phone="1",
            email="e@example.com",
        )
        self.assertEqual(club.plan, "bronce")

    def test_can_set_plan(self):
        club = Club.objects.create(
            name="Oro Club",
            city="C",
            address="A",
            phone="1",
            email="e@example.com",
            plan="oro",
        )
        self.assertEqual(club.plan, "oro")


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

    def test_plan_badge_renders_for_each_plan(self):
        """Clubs should display a plan-colored badge on search results."""
        Club.objects.create(
            name="Gold Club",
            city="NY",
            address="addr",
            phone="123",
            email="gold@example.com",
            plan="oro",
        )
        Club.objects.create(
            name="Silver Club",
            city="NY",
            address="addr",
            phone="123",
            email="silver@example.com",
            plan="plata",
        )

        url = reverse("search_results")
        response = self.client.get(url, {"q": "Club"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "badge-verified-gold")
        self.assertContains(response, "badge-verified-silver")
        self.assertContains(response, "badge-verified-bronze")

    def test_breadcrumbs_for_city(self):
        Club.objects.create(
            name="Sevilla Club",
            city="Sevilla",
            region="Andalucía",
            country="España",
            address="addr",
            phone="1",
            email="sev@example.com",
        )
        url = reverse("search_results")
        response = self.client.get(url, {"q": "Sevilla"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [c["name"] for c in response.context["breadcrumbs"]],
            ["Clubs de Sevilla", "España", "Andalucía", "Sevilla"],
        )

    def test_filter_by_region_without_query(self):
        Club.objects.create(
            name="Sevilla Club",
            city="Sevilla",
            region="Andalucía",
            country="España",
            address="addr",
            phone="1",
            email="sev@example.com",
        )
        Club.objects.create(
            name="Madrid Club",
            city="Madrid",
            region="Madrid",
            country="España",
            address="addr",
            phone="1",
            email="mad@example.com",
        )
        url = reverse("search_results")
        response = self.client.get(url, {"region": "Andalucía"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sevilla Club")
        self.assertNotContains(response, "Madrid Club")

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
        url = reverse('club_dashboard')
        res = self.client.get(url, {'estado': 'activo'})
        self.assertContains(res, 'Ana')
        self.assertNotContains(res, 'Luis')

    def test_filter_by_pago(self):
        url = reverse('club_dashboard')
        res = self.client.get(url, {'pago': 'completo'})
        self.assertContains(res, 'Ana')
        self.assertNotContains(res, 'Luis')

    def test_order_alpha(self):
        url = reverse('club_dashboard')
        res = self.client.get(url, {'orden': 'alpha'})
        members = list(res.context['members'])
        self.assertEqual(members[0], self.member1)

class DashboardMatchmakerTests(TestCase):
    def setUp(self):
        Group.objects.get_or_create(name='ClubOwner')
        self.owner1 = User.objects.create_user(username='owner1', password='pass')
        self.owner2 = User.objects.create_user(username='owner2', password='pass')
        self.club1 = Club.objects.create(
            name='Club One', city='City1', address='A1', phone='1', email='1@e.com', owner=self.owner1
        )
        self.club2 = Club.objects.create(
            name='Club Two', city='City2', address='A2', phone='2', email='2@e.com', owner=self.owner2
        )
        self.comp1 = Competidor.objects.create(
            club=self.club1,
            nombre='Alice', apellidos='A', sexo='F', peso_kg=55, edad=24
        )
        self.comp2 = Competidor.objects.create(
            club=self.club2,
            nombre='Bob', apellidos='B', sexo='M', peso_kg=70, edad=29
        )
        self.client.login(username='owner1', password='pass')

    def test_matchmaker_search_across_clubs(self):
        url = reverse('club_dashboard')
        res = self.client.get(url, {'mm_sexo': 'M'})
        self.assertContains(res, 'Bob')
        names = [c.nombre for c in res.context['match_results']]
        self.assertNotIn('Alice', names)

    def test_matchmaker_city_dropdown_lists_all_cities(self):
        """City options should include cities beyond those with clubs."""
        url = reverse('club_dashboard')
        res = self.client.get(url)
        self.assertIn('Madrid', res.context['cities'])

    def test_bookmark_competidor_persists(self):
        url = reverse('matchmaker_bookmark')
        self.client.post(url, {
            'competidor_id': self.comp2.id,
            'action': 'add'
        })
        self.club1.refresh_from_db()
        self.assertIn(self.comp2, self.club1.bookmarked_competidores.all())

    def test_remove_bookmark(self):
        self.club1.bookmarked_competidores.add(self.comp2)
        url = reverse('matchmaker_bookmark')
        self.client.post(url, {
            'competidor_id': self.comp2.id,
            'action': 'remove'
        })
        self.club1.refresh_from_db()
        self.assertNotIn(self.comp2, self.club1.bookmarked_competidores.all())


class MessageInboxTests(TestCase):
    def setUp(self):
        Group.objects.get_or_create(name='ClubOwner')
        self.owner = User.objects.create_user(username='owner', password='pass')
        self.user = User.objects.create_user(username='user', password='pass')
        self.club = Club.objects.create(
            name='Club', city='C', address='A', phone='1', email='e@e.com', owner=self.owner
        )
        ClubMessage.objects.create(club=self.club, user=self.user, content='hola')

    def test_user_message_appears_in_owner_inbox(self):
        self.client.login(username='owner', password='pass')
        url = reverse('conversation')
        res = self.client.get(url)
        self.assertContains(res, 'hola')


class MessageConversationTests(TestCase):
    def setUp(self):
        Group.objects.get_or_create(name='ClubOwner')
        self.owner = User.objects.create_user(username='owner2', password='pass')
        self.user = User.objects.create_user(username='normal', password='pass')
        self.club = Club.objects.create(
            name='Club Test', city='CT', address='Addr', phone='1', email='c@e.com', owner=self.owner
        )

    def test_non_owner_can_send_message(self):
        self.client.login(username='normal', password='pass')
        url = reverse('conversation') + f'?club={self.club.slug}'
        self.client.post(url, {'content': 'hi'})
        msg = ClubMessage.objects.latest('id')
        self.assertEqual(msg.user, self.user)
        self.assertFalse(msg.sender_is_club)

    def test_message_visible_in_inboxes(self):
        self.client.login(username='normal', password='pass')
        url = reverse('conversation') + f'?club={self.club.slug}'
        self.client.post(url, {'content': 'hello'})
        self.client.logout()

        self.client.login(username='owner2', password='pass')
        owner_inbox = self.client.get(reverse('conversation'))
        self.assertContains(owner_inbox, 'hello')

        self.client.logout()
        self.client.login(username='normal', password='pass')
        user_inbox = self.client.get(reverse('conversation'))
        self.assertContains(user_inbox, 'hello')
