
from django.core.management.base import BaseCommand
from apps.clubs.models import Club, Entrenador, TrainingLevel
from django.utils.text import slugify
import random

class Command(BaseCommand):
    help = "Genera entre 1 y 4 entrenadores por club con slugs únicos y datos ficticios"

    def handle(self, *args, **kwargs):
        first_names = [
            "Carlos", "Luis", "Miguel", "David", "Álvaro", "Raúl", "Jorge", "Pedro",
            "Andrés", "Víctor", "Sergio", "Rubén", "Antonio", "Iván", "Pablo", "Daniel",
            "Adrián", "Óscar", "Julián", "Eduardo"
        ]
        last_names = [
            "Martínez", "González", "Rodríguez", "Fernández", "López", "Sánchez", "Pérez",
            "Gómez", "Díaz", "Moreno", "Jiménez", "Ruiz", "Hernández", "Muñoz", "Álvarez",
            "Romero", "Navarro", "Torres"
        ]

        bio_template = (
            "{name} lleva más de {years} años dedicándose al boxeo, entrenando tanto a amateurs como a profesionales. "
            "Su enfoque se centra en la disciplina, la técnica y el crecimiento personal de cada alumno. "
            "Ha trabajado con atletas de diferentes edades y niveles, destacando por su trato cercano y su exigencia en cada sesión."
        )

        def get_unique_slug(nombre, apellidos):
            base_slug = slugify(f"{nombre}-{apellidos}")
            slug = base_slug
            suffix = 1
            while Entrenador.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{suffix}"
                suffix += 1
            return slug

        niveles = list(TrainingLevel.objects.all())
        clubs = Club.objects.all()
        total = 0

        Entrenador.objects.all().delete()

        for club in clubs:
            for _ in range(random.randint(1, 4)):
                nombre = random.choice(first_names)
                apellidos = random.choice(last_names)
                slug = get_unique_slug(nombre, apellidos)
                experiencia = random.randint(3, 20)
                bio = bio_template.format(name=nombre, years=experiencia)

                entrenador = Entrenador.objects.create(
                    club=club,
                    nombre=nombre,
                    apellidos=apellidos,
                    slug=slug,
                    ciudad=club.city,
                    telefono=f"6{random.randint(10000000,99999999)}",
                    whatsapp=f"6{random.randint(10000000,99999999)}",
                    email=f"{slug}@entrenadoresboxeo.com",
                    verificado=random.choice([True, False]),
                    precio_hora=random.choice([20, 25, 30, 35, 40]),
                    clase_prueba=random.choice([True, False]),
                    experiencia_anos=experiencia,
                    bio=bio
                )

                if niveles:
                    entrenador.niveles.set(random.sample(niveles, k=random.randint(1, len(niveles))))
                total += 1

        self.stdout.write(self.style.SUCCESS(f"✅ Se han creado {total} entrenadores con slugs únicos para {clubs.count()} clubes."))
