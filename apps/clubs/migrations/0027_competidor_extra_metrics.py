from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('clubs', '0026_merge_0025_merge_20250715_0837_0025_miembro_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='competidor',
            name='peso_kg',
            field=models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=2),
        ),
        migrations.AddField(
            model_name='competidor',
            name='altura_cm',
            field=models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=2),
        ),
    ]
