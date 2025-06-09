# Vistas para búsqueda de clubes, filtros, etc.
from django.shortcuts import render
from django.db.models import Q, F, FloatField, Avg, Count, ExpressionWrapper
from django.db.models.functions import Round
from apps.clubs.models import Club


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
