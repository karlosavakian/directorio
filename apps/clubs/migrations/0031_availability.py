from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0030_booking_tipo_clase'),
    ]

    operations = [
        migrations.CreateModel(
            name='Availability',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('slots', models.PositiveIntegerField(default=0)),
                ('club', models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='availabilities', to='clubs.club')),
            ],
            options={
                'ordering': ['date', 'time'],
                'unique_together': {('club', 'date', 'time')},
            },
        ),
    ]
