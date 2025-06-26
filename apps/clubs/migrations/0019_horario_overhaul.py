from django.db import migrations, models
import django.db.models.deletion


def forwards_func(apps, schema_editor):
    Horario = apps.get_model("clubs", "Horario")
    HorarioClase = apps.get_model("clubs", "HorarioClase")
    db_alias = schema_editor.connection.alias

    grupos = {}
    for horario in Horario.objects.using(db_alias).order_by("club_id", "dia", "id"):
        key = (horario.club_id, horario.dia)
        base = grupos.get(key)
        if not base:
            grupos[key] = horario
            horario.abierto = True
            horario.save(update_fields=["abierto"])
            base = horario
        HorarioClase.objects.using(db_alias).create(
            horario=base,
            hora_inicio=horario.hora_inicio,
            hora_fin=horario.hora_fin,
            texto="",
        )
        if horario.id != base.id:
            horario.delete()


def backwards_func(apps, schema_editor):
    Horario = apps.get_model("clubs", "Horario")
    HorarioClase = apps.get_model("clubs", "HorarioClase")
    db_alias = schema_editor.connection.alias

    for horario in Horario.objects.using(db_alias).order_by("club_id", "dia", "id"):
        clases = list(HorarioClase.objects.using(db_alias).filter(horario=horario))
        if not clases:
            if not horario.abierto:
                horario.delete()
            continue
        first = clases[0]
        horario.hora_inicio = first.hora_inicio
        horario.hora_fin = first.hora_fin
        horario.save(update_fields=["hora_inicio", "hora_fin"])
        for clase in clases[1:]:
            Horario.objects.using(db_alias).create(
                club_id=horario.club_id,
                dia=horario.dia,
                hora_inicio=clase.hora_inicio,
                hora_fin=clase.hora_fin,
            )
        for clase in clases:
            clase.delete()


class Migration(migrations.Migration):

    dependencies = [
        ("clubs", "0018_clubpost_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="horario",
            name="abierto",
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name="HorarioClase",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("hora_inicio", models.TimeField()),
                ("hora_fin", models.TimeField()),
                ("texto", models.CharField(blank=True, max_length=30)),
                (
                    "horario",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="clases",
                        to="clubs.horario",
                    ),
                ),
            ],
            options={
                "ordering": ["hora_inicio"],
            },
        ),
        migrations.RunPython(forwards_func, backwards_func),
        migrations.RemoveField(
            model_name="horario",
            name="hora_fin",
        ),
        migrations.RemoveField(
            model_name="horario",
            name="hora_inicio",
        ),
        migrations.AlterUniqueTogether(
            name="horario",
            unique_together={("club", "dia")},
        ),
        migrations.AlterOrderWithRespectTo(
            name="horario",
            order_with_respect_to=None,
        ),
        migrations.AlterModelOptions(
            name="horario",
            options={"ordering": ["dia"]},
        ),
    ]
