from django.db import models
from user.models import User

class Task(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    status = models.CharField(max_length=20)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    created_at = models.DateTimeField(auto_now_add=True)