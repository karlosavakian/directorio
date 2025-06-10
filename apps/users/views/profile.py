from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
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

