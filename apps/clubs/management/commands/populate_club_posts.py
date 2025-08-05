
import random
from datetime import timedelta
from django.utils import timezone
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.clubs.models import Club, ClubPost

class Command(BaseCommand):
    help = "Populate club posts with only text and YouTube videos"

    def handle(self, *args, **options):
        titulos = [
            "Entrenamiento de sparring intenso",
            "Resultados del torneo local",
            "Nueva clase para principiantes",
            "Consejos de nutrición para boxeadores",
            "Análisis técnico: Jab y desplazamiento"
        ]

        contenidos_texto = [
            "Hoy tuvimos una sesión increíble con nuestros competidores más avanzados. ¡La energía estuvo por las nubes!",
            "Felicitaciones a nuestros atletas por sus actuaciones este fin de semana. Orgullo del club.",
            "Comenzamos clases especiales para nuevos integrantes. Ven y aprende desde cero.",
            "La alimentación es clave en el rendimiento. Consulta con nuestros entrenadores especializados.",
            "Revisamos técnicas esenciales en la clase de hoy. La base lo es todo en el boxeo."
        ]

        youtube_links = [
            "https://www.youtube.com/watch?v=1U9Z3CRYGr0",
            "https://www.youtube.com/watch?v=f9S3dDTE1MI",
            "https://www.youtube.com/watch?v=zLwFYH2RZNs",
            "https://www.youtube.com/watch?v=KkVs4mh3VvI",
            "https://www.youtube.com/watch?v=dyPV7FwbUVQ"
        ]

        clubs = Club.objects.all()
        usuarios = list(User.objects.all())

        if not usuarios:
            self.stdout.write(self.style.ERROR("No hay usuarios registrados."))
            return

        for club in clubs:
            for _ in range(5):
                titulo = random.choice(titulos)
                contenido = f"{random.choice(contenidos_texto)}\n\nMira este video: {random.choice(youtube_links)}"
                user = random.choice(usuarios)
                evento_fecha = timezone.now().date() + timedelta(days=random.randint(3, 30)) if random.random() > 0.5 else None

                ClubPost.objects.create(
                    club=club,
                    user=user,
                    titulo=titulo,
                    contenido=contenido,
                    evento_fecha=evento_fecha
                )

        self.stdout.write(self.style.SUCCESS("✅ ClubPosts generados correctamente."))
