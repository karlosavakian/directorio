from django.core.management.base import BaseCommand
from faker import Faker
from django.contrib.auth.models import User
from django.conf import settings
from django.core.files import File
import random
import os

from apps.clubs.models import (
    Club, ClubPhoto, Entrenador, Horario, Clase,
    Competidor, ClubPost, Reseña, Feature
)


class Command(BaseCommand):
    help = 'Genera datos de ejemplo para clubs y entidades relacionadas.'

    def handle(self, *args, **options):
        fake = Faker('es_ES')
        image_path = os.path.join(settings.STATICFILES_DIRS[0], 'img', 'register-bg.png')
        features = list(Feature.objects.all())
        if not features:
            default_names = [
                'Ring profesional', 'Zona de pesas', 'Entrenamiento funcional',
                'Clases infantiles', 'Combates semanales'
            ]
            for name in default_names:
                features.append(Feature.objects.create(name=name))

        for _ in range(100):
            club = Club.objects.create(
                name=fake.unique.company(),
                city=fake.city(),
                address=fake.address()[:255],
                phone=fake.phone_number()[:20],
                whatsapp_link=fake.url(),
                email=fake.email(),
                about=fake.paragraph(),
            )
            club.features.set(random.sample(features, random.randint(1, len(features))))

            if os.path.exists(image_path):
                for _ in range(random.randint(1, 3)):
                    with open(image_path, 'rb') as img_file:
                        ClubPhoto.objects.create(
                            club=club,
                            image=File(img_file, name=f'{fake.word()}.jpg')
                        )

            for _ in range(random.randint(2, 5)):
                Entrenador.objects.create(
                    club=club,
                    nombre=fake.first_name(),
                    apellidos=fake.last_name(),
                )

            dias = [choice[0] for choice in Horario.DiasSemana.choices]
            for _ in range(random.randint(3, 5)):
                Horario.objects.create(
                    club=club,
                    dia=random.choice(dias),
                    estado=random.choice(['abierto', 'cerrado']),
                    hora_inicio=fake.time(),
                    hora_fin=fake.time(),
                    nota=fake.word()[:20],
                )

            for _ in range(random.randint(1, 4)):
                Clase.objects.create(
                    club=club,
                    nombre=fake.word(),
                    hora_inicio=fake.time(),
                    hora_fin=fake.time(),
                )

            for _ in range(random.randint(1, 3)):
                wins = random.randint(0, 10)
                losses = random.randint(0, 5)
                draws = random.randint(0, 3)
                Competidor.objects.create(
                    club=club,
                    nombre=fake.name(),
                    record=f"{wins}-{losses}-{draws}",
                    modalidad=random.choice([c[0] for c in Competidor.MODALIDAD_CHOICES]),
                    peso=random.choice([c[0] for c in Competidor.PESO_CHOICES]),
                    sexo=random.choice([c[0] for c in Competidor.SEXO_CHOICES]),
                    palmares=fake.text(max_nb_chars=50),
                )

            for _ in range(random.randint(1, 3)):
                ClubPost.objects.create(
                    club=club,
                    user=club.owner,
                    titulo=fake.sentence(),
                    contenido=fake.paragraph(),
                    evento_fecha=fake.date_this_year(),
                )

            for _ in range(random.randint(1, 5)):
                user = User.objects.create_user(
                    username=fake.unique.user_name(),
                    email=fake.email(),
                    password='password'
                )
                Reseña.objects.create(
                    club=club,
                    usuario=user,
                    titulo=fake.sentence(),
                    instalaciones=random.randint(1, 5),
                    entrenadores=random.randint(1, 5),
                    ambiente=random.randint(1, 5),
                    calidad_precio=random.randint(1, 5),
                    variedad_clases=random.randint(1, 5),
                    comentario=fake.sentence(),
                )

        self.stdout.write(self.style.SUCCESS('Clubs generados correctamente'))

