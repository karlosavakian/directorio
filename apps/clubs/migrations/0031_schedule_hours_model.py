from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0030_booking_tipo_clase'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScheduleHour',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hora', models.TimeField()),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedule_hours', to='clubs.club')),
            ],
            options={
                'ordering': ['hora'],
                'unique_together': {('club', 'hora')},
            },
        ),
    ]
