"""
- create: ouvert (AllowAny) pour l'inscription
- list: réservé admin
- retrieve/update/destroy: soi-même ou admin
"""
from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer
from .permissions import IsSelfOrAdmin 
from rest_framework import permissions

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        """Permissions par action pour sécuriser l'accès aux profils"""
        if self.action in ['update', 'partial_update', 'destroy', 'retrieve']:
            return [IsSelfOrAdmin()]
        if self.action == 'create':
            return [permissions.AllowAny()]
        if self.action == 'list':
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        """Admin: tous les utilisateurs sinon: uniquement soi-même"""
        user = self.request.user
        if user.is_staff:
            return User.objects.all()
        return User.objects.filter(pk=user.pk)

