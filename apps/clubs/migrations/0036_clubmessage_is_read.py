from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0035_clubmessage_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='clubmessage',
            name='is_read',
            field=models.BooleanField(default=False),
        ),
    ]
