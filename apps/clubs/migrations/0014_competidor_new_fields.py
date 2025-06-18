from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0013_entrenador_fields'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='competidor',
            name='victorias',
        ),
        migrations.RemoveField(
            model_name='competidor',
            name='derrotas',
        ),
        migrations.RemoveField(
            model_name='competidor',
            name='empates',
        ),
        migrations.RemoveField(
            model_name='competidor',
            name='titulos',
        ),
        migrations.AddField(
            model_name='competidor',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='competidores/'),
        ),
        migrations.AddField(
            model_name='competidor',
            name='record',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='competidor',
            name='modalidad',
            field=models.CharField(blank=True, choices=[('elite', 'Elite'), ('joven', 'Joven'), ('junior', 'Junior'), ('schoolboy', 'Schoolboy'), ('profesional', 'Profesional')], max_length=15),
        ),
        migrations.AddField(
            model_name='competidor',
            name='peso',
            field=models.CharField(blank=True, choices=[('minimosca', 'Minimosca'), ('mosca', 'Mosca'), ('gallo', 'Gallo'), ('pluma', 'Pluma'), ('ligero', 'Ligero'), ('welter', 'W\u00e9lter'), ('superwelter', 'Superw\u00e9lter'), ('medio', 'Medio'), ('semipesado', 'Semipesado'), ('crucero', 'Crucero'), ('pesado', 'Pesado'), ('superpesado', 'Superpesado')], max_length=15),
        ),
        migrations.AddField(
            model_name='competidor',
            name='sexo',
            field=models.CharField(blank=True, choices=[('M', 'Masculino'), ('F', 'Femenino')], max_length=1),
        ),
        migrations.AddField(
            model_name='competidor',
            name='palmares',
            field=models.TextField(blank=True, verbose_name='Palmar\u00e9s'),
        ),
    ]
