from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0018_clubpost_image'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Horario',
        ),
    ]
