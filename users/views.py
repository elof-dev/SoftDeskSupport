from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer
from .permissions import IsSelfOrAdmin  # <-- importe depuis le nouveau fichier
from rest_framework.response import Response
from rest_framework import status, permissions

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy', 'retrieve']:
            return [IsSelfOrAdmin()]
        if self.action == 'create':
            return [permissions.AllowAny()]
        if self.action == 'list':
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return User.objects.all()
        return User.objects.filter(pk=user.pk)

