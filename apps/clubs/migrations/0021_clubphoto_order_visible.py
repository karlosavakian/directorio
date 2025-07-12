from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0020_clubphoto_is_main'),
    ]

    operations = [
        migrations.AddField(
            model_name='clubphoto',
            name='position',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='clubphoto',
            name='visible',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterModelOptions(
            name='clubphoto',
            options={'ordering': ['position', 'id']},
        ),
    ]
