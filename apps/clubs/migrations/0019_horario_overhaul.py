from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0018_clubpost_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='horario',
            name='hora_fin',
        ),
        migrations.RemoveField(
            model_name='horario',
            name='hora_inicio',
        ),
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

