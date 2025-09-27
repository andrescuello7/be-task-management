from .models import User
from .serializers import UserSerializer
from rest_framework import viewsets, permissions

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permissions_classes = [permissions.AllowAny]
    serializer_class = UserSerializer