from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
        ('clubs', '0031_schedule_hours_model'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookingClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100)),
                ('precio', models.DecimalField(max_digits=6, decimal_places=2)),
                ('duracion', models.PositiveIntegerField()),
                ('detalle', models.CharField(blank=True, max_length=400)),
                ('destacado', models.BooleanField(default=False)),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='booking_classes', to='clubs.club')),
            ],
            options={'ordering': ['-destacado', 'titulo']},
        ),
        migrations.AddField(
            model_name='booking',
            name='class_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bookings', to='clubs.bookingclass'),
        ),
        migrations.RemoveField(
            model_name='booking',
            name='tipo_clase',
        ),
    ]

