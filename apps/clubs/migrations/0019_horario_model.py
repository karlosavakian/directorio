from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0018_clubpost_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Horario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dia', models.CharField(choices=[('lunes', 'Lunes'), ('martes', 'Martes'), ('miercoles', 'Mi\u00e9rcoles'), ('jueves', 'Jueves'), ('viernes', 'Viernes'), ('sabado', 'S\u00e1bado'), ('domingo', 'Domingo')], max_length=10)),
                ('abierto', models.BooleanField(default=False)),
                ('hora_inicio', models.TimeField(blank=True, null=True)),
                ('hora_fin', models.TimeField(blank=True, null=True)),
                ('nota', models.CharField(blank=True, max_length=30)),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='horarios', to='clubs.club')),
            ],
            options={
                'ordering': ['dia'],
                'unique_together': {('club', 'dia')},
            },
        ),
    ]
