from django.db import migrations, models
from django.conf import settings

class Migration(migrations.Migration):
    dependencies = [
        ('clubs', '0034_clubmessage'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='clubmessage',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='liked_messages', to=settings.AUTH_USER_MODEL),
        ),
    ]
