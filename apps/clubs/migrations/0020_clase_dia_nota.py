from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('clubs', '0019_horario_extra_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='clase',
            name='dia',
            field=models.CharField(choices=[('lunes','Lunes'),('martes','Martes'),('miercoles','Miércoles'),('jueves','Jueves'),('viernes','Viernes'),('sabado','Sábado'),('domingo','Domingo')], default='lunes', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='clase',
            name='nota',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
