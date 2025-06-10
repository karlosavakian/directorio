from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User

from django.shortcuts import render, redirect

from ..forms import ProfileForm
from ..models import Profile, Follow
from django.contrib.contenttypes.models import ContentType


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
    is_following = False
    if request.user.is_authenticated and request.user != user_obj:
        ct_user = ContentType.objects.get_for_model(User)
        is_following = Follow.objects.filter(
            follower_content_type=ct_user,
            follower_object_id=request.user.id,
            followed_content_type=ct_user,
            followed_object_id=user_obj.id,
        ).exists()
    return render(request, 'users/profile_detail.html', {
        'user_obj': user_obj,
        'profile': profile_obj,
        'is_following': is_following,
    })


@login_required
def favorites(request):
    """Placeholder view for user favorites."""
    return render(request, 'users/favorites.html')


