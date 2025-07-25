from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from django.utils.dateparse import parse_date, parse_time
from ..models import ClubPost, Booking, Club, BookingClass
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
    clase_id = request.POST.get('clase_id')
    booking_class = None
    if clase_id:
        booking_class = get_object_or_404(BookingClass, pk=clase_id, club=club)
    Booking.objects.create(
        user=request.user,
        club=club,
        fecha=fecha,
        hora=hora,
        class_type=booking_class,
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
