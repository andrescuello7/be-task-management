from .models import Task
from user.models import User
from .serializers import TaskSerializer
from rest_framework import viewsets, permissions

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    permissions_classes = [permissions.IsAuthenticated]
    serializer_class = TaskSerializer

    def perform_create(self, serializer):
        user = self.request.user
        if user.is_anonymous:  
            user = User.objects.first()
        serializer.save(author=user)
