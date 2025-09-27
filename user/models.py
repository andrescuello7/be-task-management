import uuid
from django.db import models


class User(models.Model):
    username = models.CharField(max_length=200, unique=True)
    email = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)


class AuthToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="auth_token")
    key = models.CharField(max_length=255, unique=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
