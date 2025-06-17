from django.db import migrations, models
import django.db.models.deletion

def create_group(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.get_or_create(name='ClubOwner')

class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0011_entrenador'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.AddField(
            model_name='club',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='owned_clubs', to='auth.user'),
        ),
        migrations.RunPython(create_group, migrations.RunPython.noop),
    ]
