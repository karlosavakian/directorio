from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages

from ..forms import ProfileForm, AccountForm
from ..models import Profile, Follow
from apps.clubs.models import Booking, Club, Reseña

from django.contrib.contenttypes.models import ContentType
from django.db.models import F, FloatField, Avg, Count, ExpressionWrapper
from django.db.models.functions import Round
from django.core.paginator import Paginator


@login_required
def profile(request):
    profile_obj, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = AccountForm(request.POST, request.FILES, instance=profile_obj, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado exitosamente.')
            return redirect('profile')
        else:
            for error in form.errors.get('avatar', []):
                messages.error(request, error)
    else:
        form = AccountForm(instance=profile_obj, user=request.user)
    bookings = Booking.objects.filter(user=request.user).select_related('clase', 'evento')

    follower_ct = ContentType.objects.get_for_model(request.user)
    club_ct = ContentType.objects.get_for_model(Club)

    follow_qs = Follow.objects.filter(
        follower_content_type=follower_ct,
        follower_object_id=request.user.id,
        followed_content_type=club_ct,
    )
    club_ids = follow_qs.values_list('followed_object_id', flat=True)

    clubs = Club.objects.filter(id__in=club_ids)

    average_expr = ExpressionWrapper(
        (F('reseñas__instalaciones') + F('reseñas__entrenadores') +
         F('reseñas__ambiente') + F('reseñas__calidad_precio') +
         F('reseñas__variedad_clases')) / 5.0,
        output_field=FloatField(),
    )

    clubs = clubs.annotate(
        average_rating=Round(Avg(average_expr), precision=1),
        reviews_count=Count('reseñas')
    )

    favoritos_page = clubs

    user_reviews = Reseña.objects.filter(usuario=request.user)
    return render(request, 'users/profile.html', {
        'form': form,
        'profile': profile_obj,
        'bookings': bookings,
        'favoritos': favoritos_page,
        'reviews': user_reviews,
    })

def profile_detail(request, username):
    """Public profile page"""
    user_obj = get_object_or_404(User, username=username)
    profile_obj, _ = Profile.objects.get_or_create(user=user_obj)
    is_following = False
    if request.user.is_authenticated and request.user != user_obj:
        ct_user = ContentType.objects.get_for_model(User)
        is_following = Follow.objects.filter(
            follower_content_type=ct_user,
            follower_object_id=request.user.id,
            followed_content_type=ct_user,
            followed_object_id=user_obj.id,
        ).exists()
    return render(request, 'users/profile_detail.html', {
        'user_obj': user_obj,
        'profile': profile_obj,
        'is_following': is_following,
    })


@login_required
def favorites(request):
    follower_ct = ContentType.objects.get_for_model(request.user)
    club_ct = ContentType.objects.get_for_model(Club)

    follow_qs = Follow.objects.filter(
        follower_content_type=follower_ct,
        follower_object_id=request.user.id,
        followed_content_type=club_ct,
    )
    club_ids = follow_qs.values_list('followed_object_id', flat=True)

    clubs = Club.objects.filter(id__in=club_ids)

    average_expr = ExpressionWrapper(
        (F('reseñas__instalaciones') + F('reseñas__entrenadores') +
         F('reseñas__ambiente') + F('reseñas__calidad_precio') +
         F('reseñas__variedad_clases')) / 5.0,
        output_field=FloatField(),
    )

    clubs = clubs.annotate(
        average_rating=Round(Avg(average_expr), precision=1),
        reviews_count=Count('reseñas')
    )

    paginator = Paginator(clubs, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'users/favorites.html', {
        'clubs': page_obj,
        'page_obj': page_obj,
    })


