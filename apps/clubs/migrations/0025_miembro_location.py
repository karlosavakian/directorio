from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0024_miembro_extra_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='miembro',
            name='localidad',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AddField(
            model_name='miembro',
            name='codigo_postal',
            field=models.CharField(max_length=10, blank=True),
        ),
    ]
