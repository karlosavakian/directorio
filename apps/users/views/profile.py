from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout

from ..forms import AccountForm
from ..models import Profile, Follow
from apps.clubs.models import Booking, Club, Reseña
from apps.clubs.forms import ClubForm
from apps.core.forms import PlanForm

from django.contrib.contenttypes.models import ContentType
from django.db.models import F, FloatField, Avg, Count, ExpressionWrapper
from django.db.models.functions import Round
from django.core.paginator import Paginator


@login_required
def profile(request):
    profile_obj, _ = Profile.objects.get_or_create(user=request.user)
    owned_clubs = request.user.owned_clubs.all()
    club = owned_clubs.first() if owned_clubs.exists() else None
    is_owner = owned_clubs.exists()
    if request.method == 'POST':
        if 'plan' in request.POST:
            form = AccountForm(instance=profile_obj, user=request.user)
            plan_form = PlanForm(request.POST)
            club_form = ClubForm(instance=club) if club else None
            if plan_form.is_valid():
                profile_obj.plan = plan_form.cleaned_data['plan']
                profile_obj.save()
                messages.success(request, 'Plan actualizado exitosamente.')
                return redirect('profile')
        elif 'support_option' in request.POST:
            messages.success(request, 'Solicitud de soporte enviada.')
            return redirect('profile')
        else:
            data = request.POST.copy()
            if is_owner:
                data['username'] = data.get('slug', request.user.username).lstrip('@')
            form = AccountForm(data, request.FILES, instance=profile_obj, user=request.user)
            plan_form = PlanForm(initial={'plan': profile_obj.plan})
            if club:
                for field in ['slug', 'country', 'region', 'city', 'postal_code', 'street', 'number', 'door', 'prefijo', 'phone', 'email']:
                    data.setdefault(field, getattr(club, field))
                club_form = ClubForm(data, request.FILES, instance=club)
                club_valid = club_form.is_valid()
            else:
                club_form = None
                club_valid = True
            if form.is_valid():
                profile_obj = form.save()
                if club_form and club_valid:
                    club_form.save()
                request.user.profile.refresh_from_db()
                messages.success(request, 'Perfil actualizado exitosamente.')
                return redirect('profile')
            else:
                for error in form.errors.get('avatar', []):
                    messages.error(request, error)
    else:
        form = AccountForm(instance=profile_obj, user=request.user)
        plan_form = PlanForm(initial={'plan': profile_obj.plan})
        club_form = ClubForm(instance=club) if club else None
    bookings = Booking.objects.filter(user=request.user).select_related('evento')

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

    avatar_url = profile_obj.avatar.url if profile_obj.avatar else None
    if is_owner:
        first_club = owned_clubs.first()
        if first_club and first_club.logo:
            avatar_url = first_club.logo.url

    plans = [
        {
            'value': 'bronce',
            'title': 'Plan Bronce',
            'price': '0€ / mes',
            'features': [
                'Presencia básica en el directorio',
                'Publicación de eventos',
                'Acceso a valoraciones',
            ],
        },
        {
            'value': 'plata',
            'title': 'Plan Plata',
            'price': '9€ / mes',
            'features': [
                'Todos los beneficios del Plan Bronce',
                'Publicaciones ilimitadas',
                'Estadísticas básicas',
            ],
            'featured': True,
        },
        {
            'value': 'oro',
            'title': 'Plan Oro',
            'price': '19€ / mes',
            'features': [
                'Todos los beneficios del Plan Plata',
                'Badge de verificación',
                'Herramientas de marketing avanzadas',
            ],
        },
    ]

    return render(request, 'users/profile.html', {
        'form': form,
        'club_form': club_form,
        'plan_form': plan_form,
        'plans': plans,
        'current_plan': profile_obj.plan,
        'profile': profile_obj,
        'bookings': bookings,
        'favoritos': favoritos_page,
        'reviews': user_reviews,
        'owned_clubs': owned_clubs,
        'is_owner': is_owner,
        'avatar_url': avatar_url,
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
def delete_account(request):
    """Allow a logged in user to delete their account."""
    if request.method == 'POST':
        user = request.user
        user.delete()
        logout(request)
        messages.success(request, 'Cuenta eliminada exitosamente.')
        return redirect('home')

    return render(request, 'users/delete_account_confirm.html')


 
