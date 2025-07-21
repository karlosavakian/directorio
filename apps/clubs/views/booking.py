from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from ..models import ClubPost, Booking, Club
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
    Booking.objects.create(user=request.user)
    return JsonResponse({'success': True})
