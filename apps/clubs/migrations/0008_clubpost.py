from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0007_club_verified'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClubPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=200)),
                ('contenido', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('evento_fecha', models.DateField(blank=True, null=True)),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='clubs.club')),
            ],
        ),
    ]
