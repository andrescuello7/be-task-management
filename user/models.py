import uuid
from django.db import models
from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(models.Model):
    username = models.CharField(max_length=200, unique=True)
    email = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']


class AuthToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="auth_token")
    key = models.CharField(max_length=255, unique=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
