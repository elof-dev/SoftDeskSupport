from rest_framework import permissions

class IsSelfOrAdmin(permissions.BasePermission):
    """
    Permission : autorise l'accès si l'utilisateur est lui-même ou admin.
    """
    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_staff