
from django.core.management.base import BaseCommand
from apps.clubs.models import Club
import random
import re
import unicodedata

class Command(BaseCommand):
    help = "Puebla la base de datos con clubes de boxeo ficticios"

    def handle(self, *args, **kwargs):
        def simple_slugify(text):
            text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
            text = text.lower()
            text = re.sub(r'[^\w\s-]', '', text)
            return re.sub(r'[\s_-]+', '-', text).strip('-')

        CITIES = {
            "Madrid": "Comunidad de Madrid",
            "Valencia": "Comunidad Valenciana",
            "Barcelona": "Cataluña",
            "Sevilla": "Andalucía",
            "Zaragoza": "Aragón",
        }

        NAMES = [
            "Titanes", "Guerreros", "Fénix", "Leones", "Dragones", "Spartans", "Hércules",
            "Imperium", "Centuriones", "Olimpo", "Raptors", "Vulcano", "Ares", "Gladiadores"
        ]

        STREETS = [
            "Avenida Principal", "Calle Mayor", "Paseo del Deporte", "Ronda Norte",
            "Camino Viejo", "Calle Nueva", "Avenida Libertad", "Calle Real", "Gran Vía"
        ]

        PLANS = ["bronce", "plata", "oro"]

        def generate_club(city, region, index, used_slugs):
            name_base = random.choice(NAMES)
            name = f"Club Boxeo {city} {name_base}"
            base_slug = simple_slugify(name)
            slug = base_slug
            suffix = 1

            while slug in used_slugs or Club.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{suffix}"
                suffix += 1

            used_slugs.add(slug)

            return Club(
                name=name,
                slug=slug,
                category="club",
                plan=random.choice(PLANS),
                country="España",
                region=region,
                city=city,
                street=random.choice(STREETS),
                number=str(random.randint(1, 200)),
                door=random.choice(["", "Bajo", "1ºA", "2ºB"]),
                postal_code=f"28{random.randint(100,999)}",
                prefijo="+34",
                phone=f"6{random.randint(10000000, 99999999)}",
                email=f"contacto{index}@{simple_slugify(city)}boxeo.com",
                verified=random.choice([True, False]),
            )

        Club.objects.all().delete()  # Limpiar si es necesario
        used_slugs = set()
        counter = 1
        for city, region in CITIES.items():
            for _ in range(10):
                club = generate_club(city, region, counter, used_slugs)
                club.save()
                counter += 1

        self.stdout.write(self.style.SUCCESS("✅ Se han creado 50 clubes de boxeo ficticios con slugs limpios y únicos."))
