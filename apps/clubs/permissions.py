from django.contrib.auth.models import Group


def has_club_permission(user, club):
    """Return True if user can manage the given club."""
    if not user.is_authenticated:
        return False
    return (user.is_superuser or user == getattr(club, 'owner', None)
            or user.groups.filter(name='ClubOwner').exists())
