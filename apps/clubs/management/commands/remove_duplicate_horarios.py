from django.core.management.base import BaseCommand
from apps.clubs.models import Horario

class Command(BaseCommand):
    help = 'Remove duplicate entries in the horario table based on club_id and dia'

    def handle(self, *args, **kwargs):
        duplicates = (
            Horario.objects
            .values('club_id', 'dia')
            .annotate(count=models.Count('id'))
            .filter(count__gt=1)
        )

        for duplicate in duplicates:
            horarios = Horario.objects.filter(club_id=duplicate['club_id'], dia=duplicate['dia'])
            horarios_to_delete = horarios[1:]  # Keep the first entry, delete the rest
            horarios_to_delete.delete()

        self.stdout.write(self.style.SUCCESS('Successfully removed duplicate horarios'))