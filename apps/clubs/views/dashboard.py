from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden, HttpResponse
from django.template.loader import render_to_string
from django.db.models import Q, Exists, OuterRef
from django.db.models.functions import ExtractYear
from django.utils import timezone
from collections import defaultdict


from ..models import (
    Club,
    ClubPost,
    Booking,
    ClubPhoto,
    Horario,
    Competidor,
    Entrenador,
    Miembro,
    Pago,
)
from ..forms import (
    ClubForm,
    ClubPostForm,
    ClubPhotoForm,
    HorarioForm,
    CompetidorForm,
    EntrenadorForm,
    MiembroForm,
    PagoForm,
)
from ..permissions import has_club_permission


@login_required
def dashboard(request, slug):
    club = get_object_or_404(Club, slug=slug)
    # Prepara una estructura de horarios por franja horaria para mostrar
    # los días como columnas y las horas como filas
    dias_semana = club.horarios.model.DiasSemana.choices
    all_horarios = list(club.horarios.all())

    # Agrupa los horarios por día y ordénalos por hora de inicio
    horarios_por_dia = defaultdict(list)

    for h in all_horarios:
        horarios_por_dia[h.dia].append(h)

    for dia in horarios_por_dia:
        horarios_por_dia[dia].sort(key=lambda h: h.hora_inicio)
    if club.owner != request.user:
        return redirect('home')
    coaches = club.entrenadores.all()
    members = club.miembros.all()

    # Conteos para los filtros
    estado_counts = {
        'activo': members.filter(estado='activo').count(),
        'inactivo': members.filter(estado='inactivo').count(),
    }
    sexo_counts = {
        'M': members.filter(sexo='M').count(),
        'F': members.filter(sexo='F').count(),
    }
    today = timezone.now().date()
    miembros_pagados = members.filter(
        pagos__fecha__year=today.year,
        pagos__fecha__month=today.month,
    ).distinct()
    pago_counts = {
        'completo': miembros_pagados.count(),
        'pendiente': members.exclude(id__in=miembros_pagados).count(),
    }

    # --- Matchmaker ---
    # Search competitors across all registered clubs
    match_qs = Miembro.objects.select_related('club').all()
    cities = Club.objects.values_list('city', flat=True).distinct()

    mm_sexo = request.GET.get('mm_sexo')
    if mm_sexo in ['M', 'F']:
        match_qs = match_qs.filter(sexo=mm_sexo)

    mm_peso_min = request.GET.get('mm_peso_min')
    if mm_peso_min:
        match_qs = match_qs.filter(peso__gte=mm_peso_min)
    mm_peso_max = request.GET.get('mm_peso_max')
    if mm_peso_max:
        match_qs = match_qs.filter(peso__lte=mm_peso_max)

    mm_ciudad = request.GET.get('mm_ciudad')
    if mm_ciudad:
        match_qs = match_qs.filter(club__city=mm_ciudad)

    current_year = timezone.now().year
    match_qs = match_qs.annotate(
        birth_year=ExtractYear('fecha_nacimiento')
    )

    mm_edad_min = request.GET.get('mm_edad_min')
    if mm_edad_min:
        year_max = current_year - int(mm_edad_min)
        match_qs = match_qs.filter(birth_year__lte=year_max)
    mm_edad_max = request.GET.get('mm_edad_max')
    if mm_edad_max:
        year_min = current_year - int(mm_edad_max)
        match_qs = match_qs.filter(birth_year__gte=year_min)

    match_qs = match_qs.annotate(
        edad=current_year - ExtractYear('fecha_nacimiento')
    )

    # Filtros para los miembros
    estado = request.GET.get('estado')
    if estado in ['activo', 'inactivo']:
        members = members.filter(estado=estado)

    sexo = request.GET.get('sexo')
    if sexo in ['M', 'F']:
        members = members.filter(sexo=sexo)

    peso_min = request.GET.get('peso_min')
    if peso_min:
        members = members.filter(peso__gte=peso_min)
    peso_max = request.GET.get('peso_max')
    if peso_max:
        members = members.filter(peso__lte=peso_max)

    altura_min = request.GET.get('altura_min')
    if altura_min:
        members = members.filter(altura__gte=altura_min)
    altura_max = request.GET.get('altura_max')
    if altura_max:
        members = members.filter(altura__lte=altura_max)

    pago = request.GET.get('pago')
    if pago in ['completo', 'pendiente']:
        today = timezone.now().date()
        payment_qs = Pago.objects.filter(
            miembro=OuterRef('pk'),
            fecha__year=today.year,
            fecha__month=today.month,
        )
        members = members.annotate(has_payment=Exists(payment_qs))
        if pago == 'completo':
            members = members.filter(has_payment=True)
        elif pago == 'pendiente':
            members = members.filter(has_payment=False)

    search_q = request.GET.get('q', '').strip()
    if search_q:
        members = members.filter(
            Q(nombre__icontains=search_q) | Q(apellidos__icontains=search_q)
        )

    orden = request.GET.get('orden')
    if orden == 'alpha':
        members = members.order_by('nombre', 'apellidos')
    elif orden == 'alpha_desc':
        members = members.order_by('-nombre', '-apellidos')
    elif orden == 'oldest':
        members = members.order_by('fecha_inscripcion', 'id')
    elif orden == 'newest':
        members = members.order_by('-fecha_inscripcion', '-id')

    bookings = Booking.objects.filter(
        Q(evento__club=club)
    ).select_related('user', 'evento')

    form = ClubForm(instance=club)

    return render(
        request,
        'clubs/dashboard.html',
        {
            'club': club,
            'dias_semana': dias_semana,
            'horarios_por_dia': horarios_por_dia,
            'bookings': bookings,
            'form': form,
        'coaches': coaches,
        'members': members,
        'match_results': match_qs,
        'cities': cities,
        'estado_counts': estado_counts,
        'sexo_counts': sexo_counts,
        'pago_counts': pago_counts,
        },
    )
@login_required
def club_edit(request, slug):
    club = get_object_or_404(Club, slug=slug)
    if not has_club_permission(request.user, club):
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = ClubForm(request.POST, request.FILES, instance=club)
        if form.is_valid():
            form.save()
            messages.success(request, 'Club actualizado correctamente.')
            return redirect('club_dashboard', slug=club.slug)
    else:
        form = ClubForm(instance=club)
    return render(request, 'clubs/club_form.html', {'form': form, 'club': club})


@login_required
def photo_upload(request, slug):
    club = get_object_or_404(Club, slug=slug)
    if not has_club_permission(request.user, club):
        return HttpResponseForbidden()
    if request.method == 'POST':
        images = request.FILES.getlist('image')
        if not images:
            form = ClubPhotoForm(request.POST, request.FILES)
            if form.is_valid():
                photo = form.save(commit=False)
                photo.club = club
                photo.save()
        else:
            for img in images:
                ClubPhoto.objects.create(club=club, image=img)
        messages.success(request, 'Foto añadida correctamente.')
        return redirect('club_dashboard', slug=club.slug)
    form = ClubPhotoForm()
    return render(request, 'clubs/photo_form.html', {'form': form, 'club': club})


@login_required
def photo_delete(request, pk):
    photo = get_object_or_404(ClubPhoto, pk=pk)
    if not has_club_permission(request.user, photo.club):
        return HttpResponseForbidden()
    if request.method == 'POST':
        slug = photo.club.slug
        photo.delete()
        messages.success(request, 'Foto eliminada correctamente.')
        return redirect('club_dashboard', slug=slug)
    return render(request, 'clubs/photo_confirm_delete.html', {'photo': photo})


@login_required
def photo_bulk_delete(request, slug):
    club = get_object_or_404(Club, slug=slug)
    if not has_club_permission(request.user, club):
        return HttpResponseForbidden()
    if request.method == 'POST':
        ids_str = request.POST.get('ids', '')
        ids = [int(i) for i in ids_str.split(',') if i]
        ClubPhoto.objects.filter(club=club, id__in=ids).delete()
        messages.success(request, 'Fotos eliminadas correctamente.')
    return redirect('club_dashboard', slug=club.slug)


@login_required
def photo_set_main(request, pk):
    photo = get_object_or_404(ClubPhoto, pk=pk)
    if not has_club_permission(request.user, photo.club):
        return HttpResponseForbidden()
    if request.method == 'POST':
        photo.club.photos.update(is_main=False)
        photo.is_main = True
        photo.save()
        messages.success(request, 'Foto establecida como principal.')
    return redirect('club_dashboard', slug=photo.club.slug)


@login_required
def horario_create(request, slug):
    club = get_object_or_404(Club, slug=slug)
    if not has_club_permission(request.user, club):
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = HorarioForm(request.POST)
        if form.is_valid():
            horario = form.save(commit=False)
            horario.club = club
            horario.save()
            messages.success(request, 'Horario añadido correctamente.')
            return redirect('club_dashboard', slug=club.slug)
    else:
        form = HorarioForm()
    return render(request, 'clubs/horario_form.html', {'form': form, 'club': club})


@login_required
def horario_update(request, pk):
    horario = get_object_or_404(Horario, pk=pk)
    if not has_club_permission(request.user, horario.club):
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = HorarioForm(request.POST, instance=horario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Horario actualizado correctamente.')
            return redirect('club_dashboard', slug=horario.club.slug)
    else:
        form = HorarioForm(instance=horario)
    return render(request, 'clubs/horario_form.html', {
        'form': form,
        'club': horario.club,
        'horario': horario,
    })


@login_required
def horario_delete(request, pk):
    horario = get_object_or_404(Horario, pk=pk)
    if not has_club_permission(request.user, horario.club):
        return HttpResponseForbidden()
    if request.method == 'POST':
        slug = horario.club.slug
        horario.delete()
        messages.success(request, 'Horario eliminado correctamente.')
        return redirect('club_dashboard', slug=slug)
    return render(request, 'clubs/horario_confirm_delete.html', {'horario': horario})


@login_required
def competidor_create(request, slug):
    club = get_object_or_404(Club, slug=slug)
    if not has_club_permission(request.user, club):
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = CompetidorForm(request.POST, request.FILES)
        if form.is_valid():
            competidor = form.save(commit=False)
            competidor.club = club
            competidor.save()
            messages.success(request, 'Competidor añadido correctamente.')
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return HttpResponse(status=204)
            return redirect('club_dashboard', slug=club.slug)
    else:
        form = CompetidorForm()
    template = 'clubs/_competidor_form.html' if request.headers.get('x-requested-with') == 'XMLHttpRequest' else 'clubs/competidor_form.html'
    return render(request, template, {'form': form, 'club': club})


@login_required
def competidor_update(request, pk):
    competidor = get_object_or_404(Competidor, pk=pk)
    if not has_club_permission(request.user, competidor.club):
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = CompetidorForm(request.POST, request.FILES, instance=competidor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Competidor actualizado correctamente.')
            return redirect('club_dashboard', slug=competidor.club.slug)
    else:
        form = CompetidorForm(instance=competidor)
    return render(request, 'clubs/competidor_form.html', {
        'form': form,
        'club': competidor.club,
        'competidor': competidor,
    })


@login_required
def competidor_delete(request, pk):
    competidor = get_object_or_404(Competidor, pk=pk)
    if not has_club_permission(request.user, competidor.club):
        return HttpResponseForbidden()
    if request.method == 'POST':
        slug = competidor.club.slug
        competidor.delete()
        messages.success(request, 'Competidor eliminado correctamente.')
        return redirect('club_dashboard', slug=slug)
    return render(request, 'clubs/competidor_confirm_delete.html', {
        'competidor': competidor,
    })


@login_required
def entrenador_create(request, slug):
    club = get_object_or_404(Club, slug=slug)
    if not has_club_permission(request.user, club):
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = EntrenadorForm(request.POST, request.FILES)
        if form.is_valid():
            entrenador = form.save(commit=False)
            entrenador.club = club
            entrenador.save()
            form.save_m2m()
            messages.success(request, 'Entrenador añadido correctamente.')
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return HttpResponse(status=204)
            return redirect('club_dashboard', slug=club.slug)
    else:
        form = EntrenadorForm()
    template = 'clubs/_entrenador_form.html' if request.headers.get('x-requested-with') == 'XMLHttpRequest' else 'clubs/entrenador_form.html'
    return render(request, template, {'form': form, 'club': club})


@login_required
def entrenador_update(request, pk):
    entrenador = get_object_or_404(Entrenador, pk=pk)
    if not has_club_permission(request.user, entrenador.club):
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = EntrenadorForm(request.POST, request.FILES, instance=entrenador)
        if form.is_valid():
            form.save()
            messages.success(request, 'Entrenador actualizado correctamente.')
            return redirect('club_dashboard', slug=entrenador.club.slug)
    else:
        form = EntrenadorForm(instance=entrenador)
    return render(request, 'clubs/entrenador_form.html', {
        'form': form,
        'club': entrenador.club,
        'entrenador': entrenador,
    })


@login_required
def entrenador_delete(request, pk):
    entrenador = get_object_or_404(Entrenador, pk=pk)
    if not has_club_permission(request.user, entrenador.club):
        return HttpResponseForbidden()
    if request.method == 'POST':
        slug = entrenador.club.slug
        entrenador.delete()
        messages.success(request, 'Entrenador eliminado correctamente.')
        return redirect('club_dashboard', slug=slug)
    return render(request, 'clubs/entrenador_confirm_delete.html', {
        'entrenador': entrenador,
    })


@login_required
def miembro_create(request, slug):
    club = get_object_or_404(Club, slug=slug)
    if not has_club_permission(request.user, club):
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = MiembroForm(request.POST, request.FILES)
        if form.is_valid():
            miembro = form.save(commit=False)
            miembro.club = club
            miembro.save()
            messages.success(request, 'Miembro añadido correctamente.')
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                html = render_to_string('clubs/_miembro_row.html', {'m': miembro}, request=request)
                return HttpResponse(html)
            return redirect('club_dashboard', slug=club.slug)
    else:
        form = MiembroForm()
    template = 'clubs/_miembro_form.html' if request.headers.get('x-requested-with') == 'XMLHttpRequest' else 'clubs/miembro_form.html'
    return render(request, template, {'form': form, 'club': club})


@login_required
def miembro_update(request, pk):
    miembro = get_object_or_404(Miembro, pk=pk)
    if not has_club_permission(request.user, miembro.club):
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = MiembroForm(request.POST, request.FILES, instance=miembro)
        if form.is_valid():
            form.save()
            messages.success(request, 'Miembro actualizado correctamente.')
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return HttpResponse(status=204)
            return redirect('club_dashboard', slug=miembro.club.slug)
    else:
        form = MiembroForm(instance=miembro)
    template = 'clubs/_miembro_form.html' if request.headers.get('x-requested-with') == 'XMLHttpRequest' else 'clubs/miembro_form.html'
    return render(request, template, {
        'form': form,
        'club': miembro.club,
        'miembro': miembro,
    })


@login_required
def miembro_detail(request, pk):
    miembro = get_object_or_404(Miembro, pk=pk)
    if not has_club_permission(request.user, miembro.club):
        return HttpResponseForbidden()
    return render(request, 'clubs/_miembro_detail.html', {'miembro': miembro})


@login_required
def miembro_delete(request, pk):
    miembro = get_object_or_404(Miembro, pk=pk)
    if not has_club_permission(request.user, miembro.club):
        return HttpResponseForbidden()
    if request.method == 'POST':
        slug = miembro.club.slug
        miembro.delete()
        messages.success(request, 'Miembro eliminado correctamente.')
        return redirect('club_dashboard', slug=slug)
    return render(request, 'clubs/miembro_confirm_delete.html', {
        'miembro': miembro,
    })


@login_required
def miembro_pagos(request, pk):
    miembro = get_object_or_404(Miembro, pk=pk)
    if not has_club_permission(request.user, miembro.club):
        return HttpResponseForbidden()
    pagos = miembro.pagos.all()
    form = PagoForm()
    return render(request, 'clubs/_payment_history.html', {
        'miembro': miembro,
        'pagos': pagos,
        'form': form,
    })


@login_required
def pago_create(request, miembro_id):
    miembro = get_object_or_404(Miembro, pk=miembro_id)
    if not has_club_permission(request.user, miembro.club):
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = PagoForm(request.POST)
        if form.is_valid():
            pago = form.save(commit=False)
            pago.miembro = miembro
            pago.save()
            messages.success(request, 'Pago añadido correctamente.')
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return HttpResponse(status=204)
            return redirect('club_dashboard', slug=miembro.club.slug)
    else:
        form = PagoForm()
    return render(request, 'clubs/payment_form.html', {
        'form': form,
        'miembro': miembro,
    })


@login_required
def pago_update(request, pk):
    pago = get_object_or_404(Pago, pk=pk)
    if not has_club_permission(request.user, pago.miembro.club):
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = PagoForm(request.POST, instance=pago)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pago actualizado correctamente.')
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return HttpResponse(status=204)
            return redirect('club_dashboard', slug=pago.miembro.club.slug)
    else:
        form = PagoForm(instance=pago)
    return render(request, 'clubs/payment_form.html', {
        'form': form,
        'miembro': pago.miembro,
        'pago': pago,
    })


@login_required
def pago_delete(request, pk):
    pago = get_object_or_404(Pago, pk=pk)
    if not has_club_permission(request.user, pago.miembro.club):
        return HttpResponseForbidden()
    if request.method == 'POST':
        slug = pago.miembro.club.slug
        pago.delete()
        messages.success(request, 'Pago eliminado correctamente.')
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return HttpResponse(status=204)
        return redirect('club_dashboard', slug=slug)
    return render(request, 'clubs/pago_confirm_delete.html', {'pago': pago})
