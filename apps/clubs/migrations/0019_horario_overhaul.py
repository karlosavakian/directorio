from django.db import migrations, models
import django.db.models.deletion


def copy_horarios_to_clases(apps, schema_editor):
    Horario = apps.get_model('clubs', 'Horario')
    HorarioClase = apps.get_model('clubs', 'HorarioClase')
    db_alias = schema_editor.connection.alias

    mapping = {}
    for h in Horario.objects.using(db_alias).all().order_by('club_id', 'dia', 'id'):
        key = (h.club_id, h.dia)
        if key not in mapping:
            base = h
            base.abierto = True
            base.save(update_fields=['abierto'])
            mapping[key] = base
        else:
            base = mapping[key]
        HorarioClase.objects.using(db_alias).create(
            horario=base,
            hora_inicio=h.hora_inicio,
            hora_fin=h.hora_fin,
            texto='',
        )
        if base != h:
            h.delete()

class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0018_clubpost_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='horario',
            name='abierto',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='HorarioClase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hora_inicio', models.TimeField()),
                ('hora_fin', models.TimeField()),
                ('texto', models.CharField(blank=True, max_length=30)),
                ('horario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clases', to='clubs.horario')),
            ],
            options={
                'ordering': ['hora_inicio'],
            },
        ),
        migrations.RunPython('copy_horarios_to_clases', reverse_code=migrations.RunPython.noop),
        migrations.RemoveField(
            model_name='horario',
            name='hora_fin',
        ),
        migrations.RemoveField(
            model_name='horario',
            name='hora_inicio',
        ),
        migrations.AlterUniqueTogether(
            name='horario',
            unique_together={('club', 'dia')},
        ),
        migrations.AlterOrderWithRespectTo(
            name='horario',
            order_with_respect_to=None,
        ),
        migrations.AlterModelOptions(
            name='horario',
            options={'ordering': ['dia']},
        ),
    ]

