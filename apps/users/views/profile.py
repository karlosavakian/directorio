from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from ..forms import ProfileForm
from ..models import Profile


@login_required
def profile(request):
    profile_obj, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile_obj)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile_obj)
    return render(request, 'users/profile.html', {
        'form': form,
        'profile': profile_obj,
    })


def profile_detail(request, username):
    """Public profile page"""
    user_obj = get_object_or_404(User, username=username)
    profile_obj, _ = Profile.objects.get_or_create(user=user_obj)
    return render(request, 'users/profile_detail.html', {
        'user_obj': user_obj,
        'profile': profile_obj,
    })


@login_required
def favorites(request):
    """Placeholder view for user favorites."""
    return render(request, 'users/favorites.html')

