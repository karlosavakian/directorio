from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0020_clubphoto_is_main'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReseñaPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='review_photos/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('reseña', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='clubs.reseña')),
            ],
        ),
    ]

