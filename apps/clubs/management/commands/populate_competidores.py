
from django.core.management.base import BaseCommand
from apps.clubs.models import Club, Competidor
import random

class Command(BaseCommand):
    help = "Genera competidores ficticios con nombre completo y algunos con palmarés"

    def handle(self, *args, **kwargs):
        first_names = ['Álvaro', 'Carlos', 'Javier', 'Lucía', 'María', 'Nerea', 'Pedro', 'Sara', 'Diego', 'Carmen', 'Hugo', 'Martina', 'Daniel', 'Paula', 'Sergio', 'Ana', 'Adrián', 'Laura', 'Iván', 'Elena']
        last_names = ['Sánchez', 'Gómez', 'Fernández', 'López', 'Martínez', 'Pérez', 'García', 'Romero', 'Ruiz', 'Jiménez', 'Díaz', 'Hernández', 'Muñoz', 'Álvarez', 'Moreno', 'Navarro']
        modalidades = ['schoolboy', 'junior', 'joven', 'elite', 'profesional']
        pesos = ['minimosca', 'mosca', 'gallo', 'pluma', 'ligero', 'welter', 'superwelter', 'medio', 'semipesado', 'crucero', 'pesado', 'superpesado']
        sexos = ['M', 'F']

        def generate_record():
            wins = random.randint(0, 30)
            losses = random.randint(0, 10 if wins > 0 else 5)
            draws = random.randint(0, 5)
            return f"{wins}-{losses}-{draws}"

        palmares_opciones = [
            "",
            "Participación en campeonatos regionales.",
            "Subcampeón nacional juvenil 2023.",
            "Oro en torneo interclubes 2022.",
            "Clasificado para campeonato europeo.",
            "Más de 10 victorias amateur."
        ]

        Competidor.objects.all().delete()
        total = 0
        used_names = set()

        for club in Club.objects.all():
            for _ in range(random.randint(2, 6)):
                while True:
                    nombre = random.choice(first_names)
                    apellidos = random.choice(last_names)
                    full_name = f"{nombre} {apellidos}"
                    if full_name not in used_names:
                        used_names.add(full_name)
                        break

                edad = random.randint(13, 35)
                peso_cat = random.choice(pesos)
                modalidad = (
                    "schoolboy" if edad <= 14 else
                    "junior" if edad <= 16 else
                    "joven" if edad <= 18 else
                    random.choice(["elite", "profesional"])
                )
                sexo = random.choice(sexos)

                Competidor.objects.create(
                    club=club,
                    nombre=nombre,
                    apellidos=apellidos,
                    edad=edad,
                    record=generate_record(),
                    modalidad=modalidad,
                    peso=peso_cat,
                    sexo=sexo,
                    peso_kg=round(random.uniform(48.0, 91.0), 2),
                    altura_cm=round(random.uniform(155.0, 195.0), 2),
                    palmares=random.choice(palmares_opciones)
                )
                total += 1

        self.stdout.write(self.style.SUCCESS(f"✅ Se han creado {total} competidores únicos, algunos con palmarés."))
