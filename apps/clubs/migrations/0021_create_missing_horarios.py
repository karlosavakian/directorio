from django.db import migrations
from datetime import time

def create_horarios(apps, schema_editor):
    Horario = apps.get_model('clubs', 'Horario')
    Club = apps.get_model('clubs', 'Club')
    dias = [choice[0] for choice in Horario.DiasSemana.choices]
    for club in Club.objects.all():
        existing = set(Horario.objects.filter(club=club).values_list('dia', flat=True))
        for dia in dias:
            if dia not in existing:
                Horario.objects.create(
                    club=club,
                    dia=dia,
                    estado='abierto',
                    hora_inicio=time(9, 0),
                    hora_fin=time(17, 0),
                )

class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0020_horario_estado'),
    ]

    operations = [
        migrations.RunPython(create_horarios, migrations.RunPython.noop),
    ]
