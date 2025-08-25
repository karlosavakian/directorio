from django.test import TestCase, override_settings
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from apps.clubs.models import Feature, Club, CoachFeature
from apps.core.forms import ProRegisterForm
from io import BytesIO
from PIL import Image
import tempfile

class RegistroProfesionalTests(TestCase):
    def _create_image(self):
        buf = BytesIO()
        Image.new("RGB", (1, 1)).save(buf, format="JPEG")
        buf.seek(0)
        return SimpleUploadedFile("test.jpg", buf.read(), content_type="image/jpeg")

    @override_settings(MEDIA_ROOT=tempfile.mkdtemp())
    def test_entrenador_creates_club_and_updates_profile(self):
        features = [Feature.objects.create(name=f"Feature {i}") for i in range(3)]
        coach_features = [CoachFeature.objects.create(name=f"CoachFeature {i}") for i in range(3)]
        user = User.objects.create_user(username="olduser", password="pass", email="old@example.com")
        self.client.login(username="olduser", password="pass")

        url = reverse("registro_profesional")
        data = {
            "tipo": "entrenador",
            "plan": "oro",
            "nombre": "Juan",
            "apellidos": "Perez",
            "fecha_nacimiento": "1990-01-01",
            "dni": "12345678Z",
            "prefijo": "+34",
            "telefono": "612345678",
            "sexo": "hombre",
            "pais": "España",
            "comunidad_autonoma": "Madrid",
            "ciudad": "Madrid",
            "calle": "Calle Falsa",
            "numero": 1,
            "puerta": 1,
            "codigo_postal": "28001",
            "username": "newuser",
            "name": "Club Coach",
            "about": "Algo",
            "features": [str(f.id) for f in features],
            "coach_features": [str(cf.id) for cf in coach_features],
            "logotipo": self._create_image(),
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)

        user.refresh_from_db()
        self.assertEqual(user.username, "newuser")
        self.assertEqual(user.profile.plan, "oro")

        club = Club.objects.get(owner=user)
        self.assertEqual(club.category, "entrenador")
        self.assertEqual(club.plan, "oro")
        self.assertEqual(club.features.count(), 3)
        self.assertTrue(club.logo)
        self.assertTrue(club.profilepic)

    def test_invalid_telefono(self):
        form = ProRegisterForm(data={
            "nombre": "Juan",
            "apellidos": "Perez",
            "fecha_nacimiento": "1990-01-01",
            "dni": "12345678Z",
            "prefijo": "+34",
            "telefono": "512345678",
            "sexo": "hombre",
            "pais": "España",
            "comunidad_autonoma": "Madrid",
            "ciudad": "Madrid",
            "calle": "Calle Falsa",
            "numero": 1,
            "puerta": 1,
            "codigo_postal": "28001",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("telefono", form.errors)

    @override_settings(MEDIA_ROOT=tempfile.mkdtemp())
    def test_club_requires_at_least_one_entrenador(self):
        features = [Feature.objects.create(name=f"Feature {i}") for i in range(3)]
        user = User.objects.create_user(username="clubuser", password="pass", email="club@example.com")
        self.client.login(username="clubuser", password="pass")

        url = reverse("registro_profesional")
        data = {
            "tipo": "club",
            "plan": "plata",
            "nombre": "Luis",
            "apellidos": "Gomez",
            "fecha_nacimiento": "1990-01-01",
            "dni": "12345678Z",
            "prefijo": "+34",
            "telefono": "612345678",
            "sexo": "hombre",
            "pais": "España",
            "comunidad_autonoma": "Madrid",
            "ciudad": "Madrid",
            "calle": "Calle Falsa",
            "numero": 1,
            "puerta": 1,
            "codigo_postal": "28001",
            "username": "clubuser",
            "name": "Club Test",
            "about": "Bio",
            "features": [str(f.id) for f in features],
            "logotipo": self._create_image(),
            "coaches-TOTAL_FORMS": "1",
            "coaches-INITIAL_FORMS": "0",
            "coaches-MIN_NUM_FORMS": "1",
            "coaches-MAX_NUM_FORMS": "1000",
            "coaches-0-nombre": "Pedro",
            "coaches-0-apellidos": "López",
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        club = Club.objects.get(owner=user)
        self.assertEqual(club.category, "club")
        self.assertEqual(club.entrenadores.count(), 1)
        coach = club.entrenadores.first()
        self.assertEqual(coach.nombre, "Pedro")
        self.assertTrue(club.logo)
        self.assertTrue(club.profilepic)
