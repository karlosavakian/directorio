
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.clubs.models import Club, Reseña
import random

class Command(BaseCommand):
    help = "Genera reseñas ficticias para cada club (5 por club)"

    def handle(self, *args, **kwargs):
        TITULOS = ['Entrenamiento de calidad', 'Ambiente familiar', 'Ideal para competir', 'Buenas instalaciones', 'Gran variedad de clases', 'Volveré sin duda', 'Excelente relación calidad/precio', 'Perfecto para iniciarse', 'Muy profesionales', 'Una experiencia brutal']
        COMENTARIOS = ['Los entrenadores están muy preparados y atentos.', 'El gimnasio tiene todo el equipo necesario y está limpio.', 'Buena variedad de horarios, aunque algo llenos.', 'Hay un gran ambiente entre los miembros.', 'Precios razonables por la calidad del servicio.', 'Recomendado tanto para amateurs como para avanzados.', 'Las clases son intensas y muy completas.', 'Buen lugar para aprender técnica desde cero.', 'Ideal para sacar el estrés del día a día.', '¡Me he apuntado ya para el próximo mes!']

        usuarios = list(User.objects.all())
        if len(usuarios) < 10:
            self.stdout.write(self.style.ERROR("❌ Se necesitan al menos 10 usuarios en la base de datos."))
            return

        Reseña.objects.all().delete()
        clubes = Club.objects.all()
        total = 0

        for club in clubes:
            for _ in range(5):
                usuario = random.choice(usuarios)
                Reseña.objects.create(
                    club=club,
                    usuario=usuario,
                    titulo=random.choice(TITULOS),
                    instalaciones=random.randint(3, 5),
                    entrenadores=random.randint(3, 5),
                    ambiente=random.randint(3, 5),
                    calidad_precio=random.randint(3, 5),
                    variedad_clases=random.randint(3, 5),
                    comentario=random.choice(COMENTARIOS),
                )
                total += 1

        self.stdout.write(self.style.SUCCESS(f"✅ Se han creado {total} reseñas ficticias para {clubes.count} clubes."))
