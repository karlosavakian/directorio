from django.contrib import admin
from .models import (
    Club,
    Feature,
    ClubPhoto,
    Clase,
    Competidor,
    Reseña,
    Horario,
    ClubPost,
    Entrenador,
    EntrenadorPhoto,
    TrainingLevel,
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


class HorarioInline(admin.TabularInline):
    model = Horario
    max_num = 7

    def get_extra(self, request, obj=None, **kwargs):
        if obj:
            return max(0, 7 - obj.horarios.count())
        return 7

    def get_formset(self, request, obj=None, **kwargs):
        initial = []
        if obj:
            existing = set(obj.horarios.values_list('dia', flat=True))
        else:
            existing = set()
        for dia, _ in Horario.DiasSemana.choices:
            if dia not in existing:
                initial.append({'dia': dia})
        kwargs['extra'] = len(initial)
        FormSet = super().get_formset(request, obj, **kwargs)

        class InitialFormSet(FormSet):
            def __init__(self, *args, **kw):
                kw.setdefault('initial', initial)
                super().__init__(*args, **kw)

        return InitialFormSet


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'verified', 'city', 'phone', 'email')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ClubPhotoInline, HorarioInline, ClaseInline, EntrenadorInline]
    fields = ('owner', 'logo', 'name', 'verified', 'slug', 'city', 'address', 'phone', 'whatsapp_link', 'email', 'about', 'features')

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
    list_display = ('nombre', 'club', 'dia', 'hora_inicio', 'hora_fin', 'nota')

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

