from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0030_booking_tipo_clase'),
    ]

    operations = [
        migrations.CreateModel(
            name='AvailabilitySlot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('slots', models.PositiveIntegerField(default=1)),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='availability', to='clubs.club')),
            ],
            options={
                'ordering': ['date', 'time'],
                'unique_together': {('club', 'date', 'time')},
            },
        ),
    ]
