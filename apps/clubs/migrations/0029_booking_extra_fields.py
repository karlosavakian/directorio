from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0028_competidor_apellidos_edad'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='club',
            field=models.ForeignKey(null=True, blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='clubs.club'),
        ),
        migrations.AddField(
            model_name='booking',
            name='fecha',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='hora',
            field=models.TimeField(null=True, blank=True),
        ),
    ]
