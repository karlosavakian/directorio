from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0023_pago_model'),
    ]

    operations = [
        migrations.AddField(
            model_name='miembro',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='miembros/'),
        ),
        migrations.AddField(
            model_name='miembro',
            name='fecha_nacimiento',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='miembro',
            name='direccion',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='miembro',
            name='sexo',
            field=models.CharField(blank=True, choices=[('M', 'Masculino'), ('F', 'Femenino')], max_length=1),
        ),
        migrations.AddField(
            model_name='miembro',
            name='peso',
            field=models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=2),
        ),
        migrations.AddField(
            model_name='miembro',
            name='altura',
            field=models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=2),
        ),
        migrations.AddField(
            model_name='miembro',
            name='nacionalidad',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='miembro',
            name='notas',
            field=models.TextField(blank=True),
        ),
    ]
