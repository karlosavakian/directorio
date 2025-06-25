from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0022_clase'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClaseHorario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hora_inicio', models.TimeField()),
                ('hora_fin', models.TimeField()),
                ('descripcion', models.CharField(blank=True, max_length=20)),
                ('horario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clases', to='clubs.horario')),
            ],
            options={'ordering': ['hora_inicio']},
        ),
        migrations.RemoveField(
            model_name='horario',
            name='hora_inicio',
        ),
        migrations.RemoveField(
            model_name='horario',
            name='hora_fin',
        ),
        migrations.AlterField(
            model_name='horario',
            name='estado',
            field=models.CharField(choices=[('abierto', 'Abierto'), ('cerrado', 'Cerrado'), ('vacaciones', 'Vacaciones'), ('competicion', 'Competición')], default='abierto', max_length=12),
        ),
        migrations.AddConstraint(
            model_name='horario',
            constraint=models.UniqueConstraint(fields=('club', 'dia'), name='unique_club_day'),
        ),
    ]
