from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0021_horario_otro'),
    ]

    operations = [
        migrations.CreateModel(
            name='Miembro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('apellidos', models.CharField(max_length=150)),
                ('telefono', models.CharField(blank=True, max_length=20)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('fecha_inscripcion', models.DateField(auto_now_add=True)),
                ('estado', models.CharField(choices=[('activo', 'Activo'), ('inactivo', 'Inactivo')], default='activo', max_length=10)),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='miembros', to='clubs.club')),
            ],
            options={
                'verbose_name': 'Miembro',
                'verbose_name_plural': 'Miembros',
                'ordering': ['-fecha_inscripcion'],
            },
        ),
    ]

