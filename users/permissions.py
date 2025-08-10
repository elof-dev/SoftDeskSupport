"""Permissions spécifiques de l'app Users."""
from rest_framework import permissions

class IsSelfOrAdmin(permissions.BasePermission):
    """Autorise l'accès si l'utilisateur cible est lui-même ou un admin."""
    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_staff