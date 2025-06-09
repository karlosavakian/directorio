# Vistas para búsqueda de clubes, filtros, etc.
from django.shortcuts import render, redirect
from django.db.models import Q, F, FloatField, Avg, Count, ExpressionWrapper
from django.db.models.functions import Round
from apps.clubs.models import Club


def search_results(request):
    search_query = request.GET.get('q', '').strip()
    selected_category = request.GET.get('category', '').strip()
    sort_option = request.GET.get('sort', '').strip()

    # Rechazar búsquedas vacías o demasiado cortas
    if not search_query or len(search_query) < 3:
        return redirect('home')

    # Base queryset solo clubes
    clubs = Club.objects.all()

    # Búsqueda textual flexible
    clubs = clubs.filter(
        Q(name__icontains=search_query) |
        Q(city__icontains=search_query) |
        Q(address__icontains=search_query)
    )

    # Filtro por categoría si se proporciona
    if selected_category:
        clubs = clubs.filter(category=selected_category)

    # Cálculo de nota media por reseñas
    average_expr = ExpressionWrapper(
        (F('reseñas__instalaciones') + F('reseñas__entrenadores') +
         F('reseñas__ambiente') + F('reseñas__calidad_precio') +
         F('reseñas__variedad_clases')) / 5.0,
        output_field=FloatField()
    )

    clubs = clubs.annotate(
        average_rating=Round(Avg(average_expr), precision=1),
        reviews_count=Count('reseñas')
    )

    # Ordenamientos
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