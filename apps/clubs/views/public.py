from django.shortcuts import render, get_object_or_404, redirect 
from ..models import Club, Entrenador
from django.contrib import messages
from apps.clubs.forms import ReseñaForm, ClubPostForm, ClubPostReplyForm
from apps.users.forms import RegistroUsuarioForm
from apps.users.models import Follow
from django.contrib.contenttypes.models import ContentType


def club_profile(request, slug):
    club = get_object_or_404(Club, slug=slug)
    reseñas = club.reseñas.select_related('usuario__profile', 'usuario').all()
    detallado = club.get_detailed_ratings()
    competidores = club.competidores.all()
    posts = club.posts.filter(parent__isnull=True).select_related('user').prefetch_related('replies__user')
    orden = request.GET.get('orden', 'relevantes')
    club_followed = False
    if request.user.is_authenticated:
        ct_user = ContentType.objects.get_for_model(request.user)
        ct_club = ContentType.objects.get_for_model(Club)
        club_followed = Follow.objects.filter(
            follower_content_type=ct_user,
            follower_object_id=request.user.id,
            followed_content_type=ct_club,
            followed_object_id=club.id,
        ).exists()

    reseña_existente = None
    if request.user.is_authenticated:
        reseña_existente = club.reseñas.filter(usuario=request.user).first()


    form = ReseñaForm()
    post_form = ClubPostForm()
    reply_form = ClubPostReplyForm()
    register_form = RegistroUsuarioForm()
    if request.method == 'POST' and not reseña_existente:
        form = ReseñaForm(request.POST)
        if form.is_valid():
            nueva = form.save(commit=False)
            nueva.club = club
            nueva.usuario = request.user
            nueva.save()
            messages.success(request, "Gracias por tu valoración, será publicada en breve.")
            return redirect('club_profile', slug=club.slug)

        
        
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
        'posts': posts,
        'form': form,
        'post_form': post_form,
        'reply_form': reply_form,
        'reseña_existente': reseña_existente,
        'detallado': detallado,
        'competidores': competidores,
        'club_followed': club_followed,
        'register_form': register_form,

    })


def coach_profile(request, slug):
    """Vista pública del perfil del entrenador."""
    coach = get_object_or_404(Entrenador, slug=slug)
    return render(request, 'clubs/coach_profile.html', {
        'coach': coach,
    })


def ajax_reviews(request, slug):
    """Devolver la lista de reseñas ordenada sin recargar la página."""
    club = get_object_or_404(Club, slug=slug)
    reseñas = club.reseñas.select_related('usuario__profile', 'usuario').all()
    orden = request.GET.get('orden', 'relevantes')

    if orden == 'recientes':
        reseñas = reseñas.order_by('-creado')
    elif orden == 'antiguos':
        reseñas = reseñas.order_by('creado')
    elif orden == 'puntuacion_alta':
        reseñas = sorted(reseñas, key=lambda r: r.promedio(), reverse=True)
    elif orden == 'puntuacion_baja':
        reseñas = sorted(reseñas, key=lambda r: r.promedio())
    else:
        reseñas = reseñas.order_by('-creado')

    return render(request, 'clubs/reviews_list.html', {'reseñas': reseñas})
