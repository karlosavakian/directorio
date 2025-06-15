# apps/core/mixins/permissions.py
from django.contrib.auth.mixins import UserPassesTestMixin

class IsAdminMixin(UserPassesTestMixin):
    """ Permite acceso solo a administradores """
    def test_func(self):
        return self.request.user.is_superuser
