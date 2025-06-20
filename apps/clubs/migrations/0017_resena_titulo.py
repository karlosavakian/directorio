from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0016_clubpost_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='reseña',
            name='titulo',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]