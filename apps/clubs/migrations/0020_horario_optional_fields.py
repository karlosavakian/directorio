from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0019_horario_estado_comentario'),
    ]

    operations = [
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
        migrations.AlterField(
            model_name='horario',
            name='estado',
            field=models.CharField(blank=True, choices=[('abierto', 'Abierto'), ('cerrado', 'Cerrado')], max_length=8),
        ),
    ]
