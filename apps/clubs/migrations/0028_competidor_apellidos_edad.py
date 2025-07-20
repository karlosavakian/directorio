from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('clubs', '0027_competidor_extra_metrics'),
    ]

    operations = [
        migrations.AddField(
            model_name='competidor',
            name='apellidos',
            field=models.CharField(max_length=150, blank=True),
        ),
        migrations.AddField(
            model_name='competidor',
            name='edad',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
    ]
