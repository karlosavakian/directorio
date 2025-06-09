from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0006_horario'),
    ]

    operations = [
        migrations.AddField(
            model_name='club',
            name='verified',
            field=models.BooleanField(default=False),
        ),
    ]
