from rest_framework import serializers
from .models import Task
from user.serializers import UserSerializer

class TaskSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    
    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'status', 'author', 'created_at')
        read_only_fields = ('created_at', )