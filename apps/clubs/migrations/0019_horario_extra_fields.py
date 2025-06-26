from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0018_clubpost_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='horario',
            name='descripcion',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='horario',
            name='estado',
            field=models.CharField(choices=[('abierto', 'Abierto'), ('cerrado', 'Cerrado')], default='abierto', max_length=8),
            preserve_default=False,
        ),
    ]

