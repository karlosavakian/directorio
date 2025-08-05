
from django.core.management.base import BaseCommand
from apps.clubs.models import Club, Horario
from datetime import time, timedelta

class Command(BaseCommand):
    help = "Genera horarios realistas para cada club: 4 clases diarias de lunes a viernes, cerrado fines de semana."

    def handle(self, *args, **kwargs):
        Horario.objects.all().delete()
        total = 0

        dias_semana = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]

        # Generador de horarios fijos: 09:00, 12:00, 17:00, 20:00 (cada uno 1h)
        bloques = [time(9, 0), time(12, 0), time(17, 0), time(20, 0)]

        for club in Club.objects.all():
            for dia in dias_semana:
                if dia in ["sabado", "domingo"]:
                    # Cerrado en fines de semana (no se crean bloques, solo se marcan como cerrado)
                    Horario.objects.create(
                        club=club,
                        dia=dia,
                        hora_inicio=time(0, 0),
                        hora_fin=time(0, 0),
                        estado="cerrado"
                    )
                    total += 1
                else:
                    for hora in bloques:
                        hora_fin = (datetime.combine(datetime.today(), hora) + timedelta(hours=1)).time()
                        Horario.objects.create(
                            club=club,
                            dia=dia,
                            hora_inicio=hora,
                            hora_fin=hora_fin,
                            estado="abierto"
                        )
                        total += 1

        self.stdout.write(self.style.SUCCESS(f"✅ Se han creado {total} bloques horarios para {Club.objects.count()} clubes."))
