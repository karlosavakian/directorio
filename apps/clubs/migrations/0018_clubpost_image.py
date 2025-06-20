from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0017_resena_titulo'),
    ]

    operations = [
        migrations.AddField(
            model_name='clubpost',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='club_post_images/'),
        ),
    ]
