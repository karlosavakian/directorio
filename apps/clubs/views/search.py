# Vistas para búsqueda de clubes, filtros, etc.
from django.shortcuts import render, redirect
from django.db.models import Q, F, FloatField, Avg, Count, ExpressionWrapper
from django.db.models.functions import Round
from django.core.paginator import Paginator
from django.urls import reverse
from apps.clubs.models import Club, Entrenador
from apps.clubs.spain import REGION_PROVINCES, CITY_TO_PROVINCE

PROVINCE_TO_REGION = {p: r for r, ps in REGION_PROVINCES.items() for p in ps}
CITY_TO_REGION = {c: PROVINCE_TO_REGION.get(p) for c, p in CITY_TO_PROVINCE.items()}


def search_results(request):
    search_query = request.GET.get('q', '').strip()
    selected_category = request.GET.get('category', '').strip()
    sort_option = request.GET.get('sort', '').strip()
    country = request.GET.get('country', '').strip()
    region = request.GET.get('region', '').strip()
    city = request.GET.get('city', '').strip()

    if not city and search_query in CITY_TO_REGION:
        city = search_query
        region = region or CITY_TO_REGION.get(city, '')
        country = country or 'España'

    if not any([search_query, country, region, city]):
        return redirect('home')
    if search_query and len(search_query) < 3 and not any([country, region, city]):
        return redirect('home')

    if selected_category == 'entrenador':
        coaches = Entrenador.objects.select_related('club').filter(
            Q(nombre__icontains=search_query) |
            Q(apellidos__icontains=search_query) |
            Q(ciudad__icontains=search_query) |
            Q(club__name__icontains=search_query),
            perfil_publico=True,
        )
        if city:
            coaches = coaches.filter(ciudad__iexact=city)
        if region:
            region_filter = Q(club__region__iexact=region)
            for province in REGION_PROVINCES.get(region, []):
                region_filter |= Q(club__region__iexact=province)
            coaches = coaches.filter(region_filter)
        if country:
            coaches = coaches.filter(club__country__iexact=country)

        paginator = Paginator(coaches, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        breadcrumbs = []
        base_url = reverse('search_results')
        category_label = 'Entrenadores de Boxeo'
        # Solo el primer breadcrumb lleva q
        query_params = f"?category=entrenador"
        if search_query:
            query_params += f"&q={search_query}"
        breadcrumbs.append({'name': category_label, 'url': f"{base_url}{query_params}"})

        country_label = country or 'España'
        # NO incluir q en país ni en región
        country_params = f"?category=entrenador&country={country_label}"
        breadcrumbs.append({'name': country_label, 'url': f"{base_url}{country_params}"})
        if region:
            region_params = f"?category=entrenador&country={country_label}&region={region}"
            breadcrumbs.append({'name': region, 'url': f"{base_url}{region_params}"})
        if city:
            breadcrumbs.append({'name': city, 'url': None})

        return render(request, 'clubs/search_coaches.html', {
            'coaches': page_obj,
            'page_obj': page_obj,
            'search_query': search_query,
            'selected_category': selected_category,
            'sort_option': sort_option,
            'country': country,
            'region': region,
            'city': city,
            'breadcrumbs': breadcrumbs,
            'back_url': request.META.get('HTTP_REFERER', '/'),
        })

    # Base queryset solo clubes
    clubs = Club.objects.all()

    if search_query:
        clubs = clubs.filter(
            Q(name__icontains=search_query) |
            Q(city__icontains=search_query) |
            Q(address__icontains=search_query)
        )
    if city:
        clubs = clubs.filter(city__iexact=city)
    if region:
        region_filter = Q(region__iexact=region)
        for province in REGION_PROVINCES.get(region, []):
            region_filter |= Q(region__iexact=province)
        clubs = clubs.filter(region_filter)
    if country:
        clubs = clubs.filter(country__iexact=country)

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

    # Paginación: 12 resultados por página
    paginator = Paginator(clubs, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    breadcrumbs = []
    base_url = reverse('search_results')
    category_names = {
        'club': 'Clubs',
        'entrenador': 'Entrenadores',
        'promotor': 'Promotores',
        'servicio': 'Servicios',
    }
    category_key = selected_category or 'club'
    category_label = f"{category_names.get(category_key, category_key.title())} de Boxeo"
    # Solo el primer breadcrumb lleva q
    query_params = f"?category={category_key}"
    if search_query:
        query_params += f"&q={search_query}"
    breadcrumbs.append({'name': category_label, 'url': f"{base_url}{query_params}"})

    country_label = country or 'España'
    # NO incluir q en país ni en región
    country_params = f"?category={category_key}&country={country_label}"
    breadcrumbs.append({'name': country_label, 'url': f"{base_url}{country_params}"})
    if region:
        region_params = f"?category={category_key}&country={country_label}&region={region}"
        breadcrumbs.append({'name': region, 'url': f"{base_url}{region_params}"})
    if city:
        breadcrumbs.append({'name': city, 'url': None})

    return render(request, 'clubs/search_results.html', {
        'clubs': page_obj,
        'page_obj': page_obj,
        'search_query': search_query,
        'selected_category': selected_category,
        'sort_option': sort_option,
        'country': country,
        'region': region,
        'city': city,
        'breadcrumbs': breadcrumbs,
        'back_url': request.META.get('HTTP_REFERER', '/'),
    })