from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0019_delete_clase'),
    ]

    operations = [
        migrations.AddField(
            model_name='horario',
            name='estado',
            field=models.CharField(choices=[('abierto', 'Abierto'), ('cerrado', 'Cerrado')], default='abierto', max_length=10),
        ),
        migrations.AlterField(
            model_name='horario',
            name='hora_inicio',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='horario',
            name='hora_fin',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
