from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('clubs', '0029_booking_extra_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='tipo_clase',
            field=models.CharField(choices=[('privada','Privada'),('prueba','Prueba')], default='privada', max_length=20),
        ),
    ]
