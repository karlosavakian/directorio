from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0019_horario_estado'),
    ]

    operations = [
        migrations.AddField(
            model_name='clubphoto',
            name='is_main',
            field=models.BooleanField(default=False),
        ),
    ]
