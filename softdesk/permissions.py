from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Lecture autorisée à tous les utilisateurs authentifiés.
    Modification/suppression réservée à l'auteur de la ressource.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if hasattr(obj, 'author'):
            return obj.author == request.user
        return False