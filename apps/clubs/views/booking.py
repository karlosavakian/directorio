from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from django.utils.dateparse import parse_date, parse_time
from ..models import ClubPost, Booking, Club, AvailabilitySlot
from ..forms import BookingForm, CancelBookingForm


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
    slot = AvailabilitySlot.objects.filter(club=club, date=fecha, time=hora).first()
    if slot and slot.slots > 0:
        Booking.objects.create(
            user=request.user,
            club=club,
            fecha=fecha,
            hora=hora,
            tipo_clase=tipo_clase,
        )
        slot.slots -= 1
        slot.save()
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'no slot'}, status=400)


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
def availability_json(request, slug):
    club = get_object_or_404(Club, slug=slug)
    if club.owner != request.user:
        return JsonResponse({}, status=403)
    slots = club.availability.all()
    data = {}
    for slot in slots:
        date_str = slot.date.isoformat()
        time_str = slot.time.strftime('%H:%M')
        data.setdefault(date_str, {})[time_str] = slot.slots
    return JsonResponse(data)

@login_required
def availability_save(request, slug):
    if request.method != 'POST':
        return JsonResponse({'error': 'invalid method'}, status=400)
    club = get_object_or_404(Club, slug=slug)
    if club.owner != request.user:
        return JsonResponse({}, status=403)
    try:
        import json
        payload = json.loads(request.body.decode('utf-8'))
    except Exception:
        return JsonResponse({'error': 'invalid payload'}, status=400)
    club.availability.all().delete()
    objs = []
    for date_str, times in payload.items():
        for time_str, slots in times.items():
            objs.append(AvailabilitySlot(
                club=club,
                date=parse_date(date_str),
                time=parse_time(time_str),
                slots=slots or 0,
            ))
    AvailabilitySlot.objects.bulk_create(objs)
    return JsonResponse({'success': True})
