from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from ..models import Clase, ClubPost, Booking
from ..forms import BookingForm, CancelBookingForm


@login_required
def book_clase(request, clase_id):
    clase = get_object_or_404(Clase, pk=clase_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            Booking.objects.get_or_create(user=request.user, clase=clase)
        return redirect('club_profile', slug=clase.club.slug)
    else:
        form = BookingForm()
    return render(request, 'clubs/booking_form.html', {'form': form, 'clase': clase})


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
