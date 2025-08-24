from django.contrib import admin
from .models import (
    Club,
    Feature,
    ClubPhoto,
    Competidor,
    Reseña,
    Horario,
    ClubPost,
    Entrenador,
    EntrenadorPhoto,
    TrainingLevel,
    CoachFeature,
)

class ClubPhotoInline(admin.TabularInline):
    model = ClubPhoto
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
    extra = 1


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'owner',
        'verified',
        'plan',
        'city',
        'phone',
        'email',
    )
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ClubPhotoInline, HorarioInline, EntrenadorInline]
    fields = (
        'owner',
        'logo',
        'name',
        'verified',
        'plan',
        'slug',
        'country',
        'region',
        'city',
        'street',
        'number',
        'door',
        'postal_code',
        'prefijo',
        'phone',
        'email',
        'about',
        'features',
        'coach_features',
    )

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(CoachFeature)
class CoachFeatureAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(ClubPhoto)
class ClubPhotoAdmin(admin.ModelAdmin):
    list_display = ('club', 'uploaded_at')  



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
        'features',
    )

