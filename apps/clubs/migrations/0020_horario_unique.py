from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("clubs", "0019_horario_extra_fields"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="horario",
            constraint=models.UniqueConstraint(
                fields=["club", "dia"], name="unique_horario_por_dia"
            ),
        ),
    ]
