from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status, permissions

class IsSelfOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Autorise si l'utilisateur est lui-même ou admin
        return obj == request.user or request.user.is_staff
    
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsSelfOrAdmin()]
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        # RGPD : Vérification de l'âge
        age = request.data.get('age')
        if age is not None and int(age) < 15:
            return Response(
                {"error": "Vous devez avoir au moins 15 ans pour vous inscrire."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().create(request, *args, **kwargs)