from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0019_delete_horario'),
    ]

    operations = [
        migrations.CreateModel(
            name='DaySchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(choices=[('lunes', 'Lunes'), ('martes', 'Martes'), ('miercoles', 'Mi\u00e9rcoles'), ('jueves', 'Jueves'), ('viernes', 'Viernes'), ('sabado', 'S\u00e1bado'), ('domingo', 'Domingo')], max_length=10)),
                ('is_open', models.BooleanField(default=False)),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='day_schedules', to='clubs.club')),
            ],
            options={
                'ordering': ['day'],
                'unique_together': {('club', 'day')},
            },
        ),
        migrations.CreateModel(
            name='ClassSlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hora_inicio', models.TimeField()),
                ('hora_fin', models.TimeField()),
                ('nota', models.CharField(blank=True, max_length=20)),
                ('day_schedule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='class_slots', to='clubs.dayschedule')),
            ],
        ),
    ]

