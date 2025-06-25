from django.contrib import admin
from .models import (
    Club,
    Feature,
    ClubPhoto,
    Clase,
    Competidor,
    Reseña,
    ClubPost,
    Entrenador,
    EntrenadorPhoto,
    TrainingLevel,
    DaySchedule,
    ClassSlot,
)
from django import forms 

class ClubPhotoInline(admin.TabularInline):
    model = ClubPhoto
    extra = 1

class ClaseInline(admin.TabularInline):
    model = Clase
    extra = 1

class CompetidorInline(admin.TabularInline):
    model = Competidor
    extra = 1

class EntrenadorInline(admin.TabularInline):
    model = Entrenador
    extra = 1

class EntrenadorPhotoInline(admin.TabularInline):
    model = EntrenadorPhoto
    extra = 1

class ReseñaInline(admin.TabularInline):
    model = Reseña
    extra = 1
    readonly_fields = ('creado',)


class BaseDayScheduleInlineFormSet(forms.BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        days = [choice[0] for choice in DaySchedule.WeekDay.choices]
        existing = {form.instance.day for form in self.forms if form.instance.pk}
        remaining_days = [d for d in days if d not in existing]
        # assign remaining days to extra forms
        for form, day in zip(self.extra_forms, remaining_days):
            form.initial.setdefault('day', day)


class DayScheduleInline(admin.TabularInline):
    model = DaySchedule
    formset = BaseDayScheduleInlineFormSet
    fields = ('day', 'is_open')
    extra = 0
    max_num = 7
    show_change_link = True

    def get_extra(self, request, obj=None, **kwargs):
        if obj:
            return max(0, 7 - obj.day_schedules.count())
        return 7


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'verified', 'city', 'phone', 'email')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ClubPhotoInline, EntrenadorInline, DayScheduleInline]
    fields = (
        'owner',
        'logo',
        'name',
        'verified',
        'slug',
        'city',
        'address',
        'phone',
        'whatsapp_link',
        'email',
        'about',
        'features',
    )

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(ClubPhoto)
class ClubPhotoAdmin(admin.ModelAdmin):
    list_display = ('club', 'uploaded_at')  


class ClaseAdminForm(forms.ModelForm):
    class Meta:
        model = Clase
        fields = '__all__'
        widgets = {
            'hora_inicio': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
            'hora_fin': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
        }   
@admin.register(Clase)
class ClaseAdmin(admin.ModelAdmin):
    form = ClaseAdminForm
    list_display = ('nombre', 'club', 'hora_inicio', 'hora_fin')

@admin.register(Competidor)
class CompetidorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'club', 'record', 'modalidad', 'peso', 'sexo')

@admin.register(Reseña)
class ReseñaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'club', 'promedio', 'creado')  # ✅ Quitamos 'stars'
    readonly_fields = ('creado',)


@admin.register(ClubPost)
class ClubPostAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'club', 'user', 'created_at', 'evento_fecha')


class ClassSlotInline(admin.TabularInline):
    model = ClassSlot
    extra = 1


@admin.register(DaySchedule)
class DayScheduleAdmin(admin.ModelAdmin):
    list_display = ('club', 'day', 'is_open')
    list_filter = ('club', 'day', 'is_open')
    inlines = [ClassSlotInline]


@admin.register(Entrenador)
class EntrenadorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellidos', 'club', 'verificado')
    prepopulated_fields = {'slug': ('nombre', 'apellidos')}
    inlines = [EntrenadorPhotoInline]
    fields = (
        'club',
        'avatar',
        'nombre',
        'apellidos',
        'slug',
        'verificado',
        'ciudad',
        'telefono',
        'whatsapp',
        'email',
        'precio_hora',
        'promociones',
        'clase_prueba',
        'experiencia_anos',
        'bio',
        'niveles',
    )

