from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0021_create_missing_horarios'),
    ]

    operations = [
        migrations.CreateModel(
            name='Clase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hora_inicio', models.TimeField()),
                ('hora_fin', models.TimeField()),
                ('texto', models.CharField(blank=True, max_length=255)),
                ('horario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clases', to='clubs.horario')),
            ],
            options={'ordering': ['hora_inicio']},
        ),
    ]
