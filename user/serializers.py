from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'firstname', 'lastname', 'created_at')
        read_only_fields = ('created_at', )