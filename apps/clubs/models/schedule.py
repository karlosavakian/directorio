from django.db import models

from .club import Club


class DaySchedule(models.Model):
    class WeekDay(models.TextChoices):
        LUNES = "lunes", "Lunes"
        MARTES = "martes", "Martes"
        MIERCOLES = "miercoles", "Mi\u00e9rcoles"
        JUEVES = "jueves", "Jueves"
        VIERNES = "viernes", "Viernes"
        SABADO = "sabado", "S\u00e1bado"
        DOMINGO = "domingo", "Domingo"

    club = models.ForeignKey(Club, related_name="day_schedules", on_delete=models.CASCADE)
    day = models.CharField(max_length=10, choices=WeekDay.choices)
    is_open = models.BooleanField(default=False)

    class Meta:
        unique_together = ("club", "day")
        ordering = ["day"]

    def __str__(self):
        return f"{self.club.name} - {self.get_day_display()}"


class ClassSlot(models.Model):
    day_schedule = models.ForeignKey(DaySchedule, related_name="class_slots", on_delete=models.CASCADE)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    nota = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.day_schedule.get_day_display()} {self.hora_inicio}-{self.hora_fin}"

