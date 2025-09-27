
from django.urls import path, include

urlpatterns = [
    path('api/task/', include('task.urls')),
    path('api/user/', include('user.urls')),
]