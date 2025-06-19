from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0014_competidor_new_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='clubpost',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='club_posts', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='clubpost',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='clubs.clubpost'),
        ),
        migrations.AlterField(
            model_name='clubpost',
            name='titulo',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
