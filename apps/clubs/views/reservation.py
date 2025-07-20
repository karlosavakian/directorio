from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from ..models import Club, ClassReservation
from ..forms import ClassReservationForm


@login_required
def reserve_class(request, slug):
    club = get_object_or_404(Club, slug=slug)
    if request.method == 'POST':
        form = ClassReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.club = club
            reservation.save()
            messages.success(request, 'Reserva realizada correctamente.')
            return redirect('club_profile', slug=slug)
    return redirect('club_profile', slug=slug)
