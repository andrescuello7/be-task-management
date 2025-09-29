
from django.urls import path, include

urlpatterns = [
    path('api/tasks/', include('task.urls')),
    path('api/user/', include('user.urls')),
]