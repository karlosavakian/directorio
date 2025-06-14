from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_follow'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='notifications',
            field=models.BooleanField(default=True),
        ),
    ]
