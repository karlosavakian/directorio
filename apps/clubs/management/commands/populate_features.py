
from django.core.management.base import BaseCommand
from apps.clubs.models import Club, Feature
import random

FEATURE_NAMES = [
    "Ring", "Wi-Fi", "Pera velocidad", "Nevera", "Botellas de agua", "Parquet", "Báscula",
    "Combas", "Guantes de sparring", "Cinta de correr", "Bicicleta estática", "Pera loca",
    "Reloj Rounds", "Ventilador", "Espejo", "Aquabag", "Coquillas", "Taquillas", "Sacos",
    "Casco", "Pesas", "Entrenador", "Duchas", "Calefacción", "Aire Acondicionado"
]

class Command(BaseCommand):
    help = "Asigna al menos el 60% de las features a cada club"

    def handle(self, *args, **kwargs):
        # Crear features si no existen
        for name in FEATURE_NAMES:
            Feature.objects.get_or_create(name=name)

        features = list(Feature.objects.all())
        total_features = len(features)
        clubs = Club.objects.all()

        for club in clubs:
            num_to_assign = max(1, int(total_features * 0.6))
            selected_features = random.sample(features, num_to_assign)

            if hasattr(club, "features"):
                club.features.set(selected_features)
            else:
                self.stderr.write(self.style.ERROR(
                    f"❌ El modelo Club no tiene relación ManyToMany con Feature."
                ))
                return

        self.stdout.write(self.style.SUCCESS(
            f"✅ Features asignadas aleatoriamente a {clubs.count()} clubes"
        ))
