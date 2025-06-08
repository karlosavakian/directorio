from django.shortcuts import render, get_object_or_404, redirect 
from ..models import Club
from django.contrib import messages
from apps.users.forms import ReseñaForm


def club_profile(request, slug):
    club = get_object_or_404(Club, slug=slug)
    reseñas = club.reseñas.select_related('usuario').all()
    detallado = club.get_detailed_ratings()
    competidores = club.competidores.all()
    orden = request.GET.get('orden', 'relevantes')

    reseña_existente = None
    if request.user.is_authenticated:
        reseña_existente = club.reseñas.filter(usuario=request.user).first()

    form = ReseñaForm()
    if request.method == 'POST' and not reseña_existente:
        form = ReseñaForm(request.POST)
        if form.is_valid():
            nueva = form.save(commit=False)
            nueva.club = club
            nueva.usuario = request.user
            nueva.save()
            messages.success(request, "Gracias por tu valoración, será publicada en breve.")
            return redirect('club_profile', slug=reseña.club.slug)
        
        
    if orden == 'recientes':
        reseñas = reseñas.order_by('-creado')
    elif orden == 'antiguos':
        reseñas = reseñas.order_by('creado')
    elif orden == 'puntuacion_alta':
        reseñas = sorted(reseñas, key=lambda r: r.promedio(), reverse=True)
    elif orden == 'puntuacion_baja':
        reseñas = sorted(reseñas, key=lambda r: r.promedio())
    else:  # relevantes (por defecto)
        reseñas = reseñas.order_by('-creado')  # puedes mejorar esto más adelante

    return render(request, 'clubs/club_profile.html', {
        'club': club,
        'reseñas': reseñas,
        'form': form,
        'reseña_existente': reseña_existente,
        'detallado': detallado,
        'competidores': competidores,
        
    })
