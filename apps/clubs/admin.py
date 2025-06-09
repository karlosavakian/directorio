from django.contrib import admin
from .models import Club, Feature, ClubPhoto, Clase, Competidor, Reseña, Horario
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

class ReseñaInline(admin.TabularInline):
    model = Reseña
    extra = 1
    readonly_fields = ('creado',)


class HorarioInline(admin.TabularInline):
    model = Horario
    extra = 1


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ('name', 'verified', 'city', 'phone', 'email')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ClubPhotoInline, HorarioInline]  
    fields = ('logo', 'name', 'verified', 'slug', 'city', 'address', 'phone', 'whatsapp_link', 'email', 'about', 'features')

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
    list_display = ('nombre', 'club', 'victorias', 'derrotas', 'empates')

@admin.register(Reseña)
class ReseñaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'club', 'promedio', 'creado')  # ✅ Quitamos 'stars'
    readonly_fields = ('creado',)

