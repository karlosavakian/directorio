from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden

from django.utils.dateparse import parse_date, parse_time
from django.utils import timezone
from ..models import ClubPost, Booking, Club, Availability
import json
from ..forms import BookingForm, CancelBookingForm
from django.contrib import messages


@login_required
def cancel_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    if request.method == 'POST':
        form = CancelBookingForm(request.POST)
        if form.is_valid():
            booking.status = 'cancelled'
            booking.save()
            return redirect('profile')
    else:
        form = CancelBookingForm()
    return render(request, 'clubs/booking_cancel.html', {'form': form, 'booking': booking})


@login_required
def create_booking(request, slug):
    """Create a booking record for the current user."""
    if request.method != 'POST':
        return JsonResponse({'error': 'invalid method'}, status=400)

    club = get_object_or_404(Club, slug=slug)
    fecha = parse_date(request.POST.get('date', ''))
    hora = parse_time(request.POST.get('time', ''))
    tipo_clase = request.POST.get('tipo_clase', 'privada')
    Booking.objects.create(
        user=request.user,
        club=club,
        fecha=fecha,
        hora=hora,
        tipo_clase=tipo_clase,
    )
    return JsonResponse({'success': True})


@login_required
def booking_set_status(request, pk, status):
    """Update booking status (for club owners)."""
    booking = get_object_or_404(Booking, pk=pk)
    if booking.club and booking.club.owner != request.user:
        return redirect('home')
    if request.method == 'POST':
        booking.status = status
        booking.save()
    return redirect('club_dashboard', slug=booking.club.slug)


def booking_confirm(request, pk):
    return booking_set_status(request, pk, 'active')


def booking_cancel_admin(request, pk):
    return booking_set_status(request, pk, 'cancelled')


@login_required
def booking_delete(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if booking.club and booking.club.owner != request.user:
        return redirect('home')
    if request.method == 'POST':
        slug = booking.club.slug
        booking.delete()
        messages.success(request, 'Reserva eliminada correctamente.')
        return redirect('club_dashboard', slug=slug)
    return render(request, 'clubs/booking_confirm_delete.html', {'booking': booking})


@login_required
def save_availability(request, slug):
    if request.method != 'POST':
        return JsonResponse({'error': 'invalid method'}, status=400)
    club = get_object_or_404(Club, slug=slug)
    if club.owner != request.user:
        return HttpResponseForbidden()
    try:
        data = json.loads(request.body.decode('utf-8'))
    except ValueError:
        data = {}
    availability = data.get('availability', {})

    year = timezone.now().year

    existing = {
        (a.date, a.time): a
        for a in club.availabilities.filter(date__year=year)
    }

    new_data = {}
    for date_str, times in availability.items():
        d = parse_date(date_str)
        if not d:
            continue
        for time_str, val in times.items():
            t = parse_time(time_str)
            if t is None:
                continue
            val_int = int(val)
            if val_int > 0:
                new_data[(d, t)] = val_int

    for (d, t), slots in new_data.items():
        if (d, t) in existing:
            obj = existing[(d, t)]
            if obj.slots != slots:
                obj.slots = slots
                obj.save(update_fields=['slots'])
        else:
            Availability.objects.create(club=club, date=d, time=t, slots=slots)

    for (d, t), obj in existing.items():
        if (d, t) not in new_data:
            obj.delete()

    return JsonResponse({'success': True})
