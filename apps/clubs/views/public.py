from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from ..models import Club, Entrenador
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from apps.clubs.forms import (
    ReseñaForm,
    ClubPostForm,
    ClubPostReplyForm,
    MiembroForm,
    ClubMessageForm,
)
from apps.users.forms import RegistroUsuarioForm
from apps.users.models import Follow
from django.contrib.contenttypes.models import ContentType
from apps.clubs.spain import REGION_PROVINCES, CITY_TO_PROVINCE
from django.utils import timezone

PROVINCE_TO_REGION = {p: r for r, ps in REGION_PROVINCES.items() for p in ps}
CITY_TO_REGION = {c: PROVINCE_TO_REGION.get(p) for c, p in CITY_TO_PROVINCE.items()}


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

    # Prepare horario data for easy access in templates
    horarios = club.horarios.all()
    schedule_data = {}
    for day, _ in club.horarios.model.DiasSemana.choices:
        intervals = [
            f"{h.hora_inicio.strftime('%H:%M')}-{h.hora_fin.strftime('%H:%M')}"
            for h in horarios.filter(dia=day)
        ]
        schedule_data[day] = "|".join(intervals)

    form = ReseñaForm()
    post_form = ClubPostForm()
    reply_form = ClubPostReplyForm()
    message_form = ClubMessageForm()
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

    # Ensure the logged in user's review is shown first
    if request.user.is_authenticated:
        if not isinstance(reseñas, list):
            reseñas = list(reseñas)
        user_review = next((r for r in reseñas if r.usuario == request.user), None)
        if user_review:
            reseñas.remove(user_review)
            reseñas.insert(0, user_review)

    # Attach forms for editing
    posts = list(posts)
    for p in posts:
        p.edit_form = ClubPostForm(instance=p)

    if not isinstance(reseñas, list):
        reseñas = list(reseñas)
    for r in reseñas:
        r.edit_form = ReseñaForm(instance=r)

    base_url = reverse('search_results')
    category_label = "Clubs de Boxeo"
    query_params = "?category=club"
    breadcrumbs = [
        {'name': category_label, 'url': f"{base_url}{query_params}"}
    ]
    country_label = club.country or 'España'
    breadcrumbs.append({'name': country_label, 'url': f"{base_url}{query_params}&country={country_label}"})
    if club.region:
        region_label = PROVINCE_TO_REGION.get(club.region) or CITY_TO_REGION.get(club.city, club.region)
        breadcrumbs.append({'name': region_label, 'url': f"{base_url}{query_params}&country={country_label}&region={region_label}"})
    else:
        region_label = CITY_TO_REGION.get(club.city, '')
    if club.city:
        region_query = f"&region={region_label}" if region_label else ""
        breadcrumbs.append({'name': club.city, 'url': f"{base_url}{query_params}&country={country_label}{region_query}&city={club.city}"})
    breadcrumbs.append({'name': club.name, 'url': reverse('club_profile', args=[club.slug])})

    return render(request, 'clubs/club_profile.html', {
        'club': club,
        'reseñas': reseñas,
        'posts': posts,
        'form': form,
        'post_form': post_form,
        'reply_form': reply_form,
        'message_form': message_form,
        'reseña_existente': reseña_existente,
        'detallado': detallado,
        'competidores': competidores,
        'club_followed': club_followed,
        'register_form': register_form,
        'schedule_data': schedule_data,
        'booking_classes': club.booking_classes.all(),
        'breadcrumbs': breadcrumbs,

    })


def coach_profile(request, slug):
    """Vista pública del perfil del entrenador."""
    coach = get_object_or_404(Entrenador, slug=slug)
    coach_followed = False
    if request.user.is_authenticated:
        ct_user = ContentType.objects.get_for_model(request.user)
        ct_coach = ContentType.objects.get_for_model(Entrenador)
        coach_followed = Follow.objects.filter(
            follower_content_type=ct_user,
            follower_object_id=request.user.id,
            followed_content_type=ct_coach,
            followed_object_id=coach.id,
        ).exists()

    base_url = reverse('search_results')
    category_label = "Entrenadores de Boxeo"
    query_params = "?category=entrenador"
    breadcrumbs = [
        {'name': category_label, 'url': f"{base_url}{query_params}"}
    ]
    country_label = coach.club.country or 'España'
    breadcrumbs.append({'name': country_label, 'url': f"{base_url}{query_params}&country={country_label}"})
    if coach.club.region:
        region_label = PROVINCE_TO_REGION.get(coach.club.region) or CITY_TO_REGION.get(coach.club.city, coach.club.region)
        breadcrumbs.append({'name': region_label, 'url': f"{base_url}{query_params}&country={country_label}&region={region_label}"})
    else:
        region_label = CITY_TO_REGION.get(coach.club.city, '')
    if coach.club.city:
        region_query = f"&region={region_label}" if region_label else ""
        breadcrumbs.append({'name': coach.club.city, 'url': f"{base_url}{query_params}&country={country_label}{region_query}&city={coach.club.city}"})
    breadcrumbs.append({'name': coach.club.name, 'url': reverse('club_profile', args=[coach.club.slug])})
    breadcrumbs.append({'name': f"{coach.nombre} {coach.apellidos}", 'url': reverse('coach_profile', args=[coach.slug])})

    return render(request, 'clubs/coach_profile.html', {
        'coach': coach,
        'coach_followed': coach_followed,
        'breadcrumbs': breadcrumbs,
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

    if request.user.is_authenticated:
        if not isinstance(reseñas, list):
            reseñas = list(reseñas)
        user_review = next((r for r in reseñas if r.usuario == request.user), None)
        if user_review:
            reseñas.remove(user_review)
            reseñas.insert(0, user_review)

    if not isinstance(reseñas, list):
        reseñas = list(reseñas)
    for r in reseñas:
        r.edit_form = ReseñaForm(instance=r)

    return render(request, 'clubs/reviews_list.html', {'reseñas': reseñas})


def member_signup(request, slug):
    """Allow public users to register as club members."""
    club = get_object_or_404(Club, slug=slug)
    if request.method == 'POST':
        form = MiembroForm(
            request.POST,
            request.FILES,
        )
        if form.is_valid():
            miembro = form.save(commit=False)
            miembro.club = club
            miembro.fuente = 'directa'
            miembro.estado = 'activo'
            miembro.fecha_inscripcion = timezone.now().date()
            miembro.save()
            form.save_m2m()
            messages.success(request, 'Inscripción guardada correctamente.')
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return HttpResponse(status=204)
            return redirect('club_profile', slug=club.slug)
    else:
        form = MiembroForm()
    template = 'clubs/_miembro_public_form.html' if request.headers.get('x-requested-with') == 'XMLHttpRequest' else 'clubs/miembro_form.html'
    return render(request, template, {'form': form, 'club': club})


def booking_form(request, slug):
    """Display a simple booking form modal."""
    club = get_object_or_404(Club, slug=slug)
    return render(request, 'partials/_booking_modal.html', {'club': club})


@login_required
def send_message(request, slug):
    club = get_object_or_404(Club, slug=slug)
    form = ClubMessageForm(request.POST)
    if form.is_valid():
        msg = form.save(commit=False)
        msg.club = club
        msg.user = request.user
        msg.save()
    return redirect('club_profile', slug=slug)
