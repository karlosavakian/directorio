from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect 
from django.contrib.auth import login
from .forms import RegistroUsuarioForm
from django.contrib.auth.decorators import login_required 
from .models import Club 
from .models import Reseña 
from django.contrib import messages  
from django.db.models import Q, Count, Avg, F, ExpressionWrapper, FloatField 
from django.db.models.functions import Round
from .forms import ReseñaForm




  
from django.contrib.auth import get_user_model 

def home(request):
    search_query = request.GET.get('q', '').strip()
    return render(request, 'clubs/home.html', {
        'search_query': search_query,
    })


def register(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistroUsuarioForm()
    
    return render(request, 'registration/register.html', {'form': form})

 
def search_results(request):
    search_query = request.GET.get('q', '').strip()
    selected_category = request.GET.get('category', '').strip()
    sort_option = request.GET.get('sort', '').strip()

    clubs = Club.objects.all()

    if search_query:
        clubs = clubs.filter(
            Q(name__icontains=search_query) |
            Q(city__icontains=search_query) |
            Q(address__icontains=search_query)
        )

    if selected_category:
        clubs = clubs.filter(category=selected_category)

    average_expr = ExpressionWrapper(
        (F('reseñas__instalaciones') + F('reseñas__entrenadores') +
        F('reseñas__ambiente') + F('reseñas__calidad_precio') +
        F('reseñas__variedad_clases')) / 5.0,
        output_field=FloatField()
    )


    clubs = clubs.annotate(
        average_rating=Round(Avg(average_expr), precision=1),  # 👈 solo 1 decimal
        reviews_count=Count('reseñas')
    )

    if sort_option == 'rating':
        clubs = clubs.order_by('-average_rating')
    elif sort_option == 'reviews':
        clubs = clubs.order_by('-reviews_count')
    elif sort_option == 'recent':
        clubs = clubs.order_by('-created_at')

    return render(request, 'clubs/search_results.html', {
        'clubs': clubs,
        'search_query': search_query,
        'selected_category': selected_category,
        'sort_option': sort_option,
        'back_url': request.META.get('HTTP_REFERER', '/'),
    }) 



def club_profile(request, slug):
    club = get_object_or_404(Club, slug=slug)
    reseñas = club.reseñas.select_related('usuario').all()
    detallado = club.get_detailed_ratings()

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
            return redirect('club_profile', slug=slug)

    return render(request, 'clubs/club_profile.html', {
        'club': club,
        'reseñas': reseñas,
        'form': form,
        'reseña_existente': reseña_existente,
        'detallado': detallado,
        
    })


@login_required
def dejar_reseña(request, slug):
    club = get_object_or_404(Club, slug=slug)

    if request.method == 'POST':
        form = ReseñaForm(request.POST)
        if form.is_valid():
            reseña = form.save(commit=False)
            reseña.club = club
            reseña.usuario = request.user
            reseña.stars = reseña.promedio()  # nota calculada automáticamente
            reseña.save()
            messages.success(request, '¡Gracias por dejar tu reseña!')
            return redirect('club_profile', slug=slug)
    else:
        form = ReseñaForm()

    return render(request, 'clubs/dejar_reseña.html', {'club': club, 'form': form})


@login_required
def editar_reseña(request, reseña_id):
    reseña = get_object_or_404(Reseña, id=reseña_id, usuario=request.user)
    if request.method == 'POST':
        form = ReseñaForm(request.POST, instance=reseña)
        if form.is_valid():
            form.save()
            return redirect('club_profile', slug=reseña.club.slug)
    else:
        form = ReseñaForm(instance=reseña)
    return render(request, 'clubs/editar_reseña.html', {'form': form, 'reseña': reseña})

@login_required
def eliminar_reseña(request, reseña_id):
    reseña = get_object_or_404(Reseña, id=reseña_id, usuario=request.user)
    club_slug = reseña.club.slug
    if request.method == 'POST':
        reseña.delete()
        return redirect('club_profile', slug=club_slug)

@login_required
def mis_reseñas(request):
    reseñas = Reseña.objects.filter(usuario=request.user)
    return render(request, 'clubs/mis_reseñas.html', {'reseñas': reseñas})