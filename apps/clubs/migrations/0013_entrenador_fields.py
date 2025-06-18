from django.db import migrations, models
import django.db.models.deletion
from django.utils.text import slugify


def populate_slugs(apps, schema_editor):
    Entrenador = apps.get_model('clubs', 'Entrenador')
    for coach in Entrenador.objects.all():
        if coach.slug:
            continue
        base_slug = slugify(f"{coach.nombre}-{coach.apellidos}")
        slug = base_slug
        counter = 1
        while Entrenador.objects.filter(slug=slug).exclude(pk=coach.pk).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        coach.slug = slug
        coach.save()


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0012_club_owner'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrainingLevel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'verbose_name': 'Nivel',
                'verbose_name_plural': 'Niveles',
            },
        ),
        migrations.AddField(
            model_name='entrenador',
            name='slug',
            field=models.SlugField(blank=True, default='', editable=False),
        ),
        migrations.AddField(
            model_name='entrenador',
            name='ciudad',
            field=models.CharField(blank=True, choices=[('Madrid', 'Madrid'), ('Barcelona', 'Barcelona'), ('Valencia', 'Valencia'), ('Sevilla', 'Sevilla'), ('Zaragoza', 'Zaragoza')], max_length=50),
        ),
        migrations.AddField(
            model_name='entrenador',
            name='telefono',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='entrenador',
            name='whatsapp',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='entrenador',
            name='email',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name='entrenador',
            name='verificado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='entrenador',
            name='precio_hora',
            field=models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=6),
        ),
        migrations.AddField(
            model_name='entrenador',
            name='promociones',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='entrenador',
            name='clase_prueba',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='entrenador',
            name='experiencia_anos',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='entrenador',
            name='bio',
            field=models.TextField(blank=True),
        ),
        migrations.CreateModel(
            name='EntrenadorPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='coach_photos/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('entrenador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='clubs.entrenador')),
            ],
        ),
        migrations.AddField(
            model_name='entrenador',
            name='niveles',
            field=models.ManyToManyField(blank=True, to='clubs.traininglevel'),
        ),
        migrations.RunPython(populate_slugs, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='entrenador',
            name='slug',
            field=models.SlugField(blank=True, unique=True, editable=False),
        ),
    ]
