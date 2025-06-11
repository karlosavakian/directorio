from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0010_merge_0009_alter_clubpost_options_0009_booking'),
    ]

    operations = [
        migrations.CreateModel(
            name='Entrenador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='entrenadores/')),
                ('nombre', models.CharField(max_length=100)),
                ('apellidos', models.CharField(max_length=150)),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entrenadores', to='clubs.club')),
            ],
        ),
    ]
