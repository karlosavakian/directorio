from django.test import TestCase, override_settings
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from apps.clubs.models import Feature, Club
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
        feature = Feature.objects.create(name="Ring")
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
            "features": [str(feature.id)],
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
        self.assertEqual(club.features.count(), 1)
