from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import BasePermission


class DenyPermission(BasePermission):
    message = _("You have no access for create")

    def has_permission(self, request, view):
        return False
