from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0020_clubphoto_is_main'),
    ]

    operations = [
        migrations.AlterField(
            model_name='horario',
            name='estado',
            field=models.CharField(choices=[('abierto', 'Abierto'), ('cerrado', 'Cerrado'), ('otro', 'Otro')], default='abierto', max_length=10),
        ),
        migrations.AddField(
            model_name='horario',
            name='estado_otro',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
