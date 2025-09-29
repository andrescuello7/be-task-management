from django.urls import path
from user.api import UserViewSet
from user.views import auth_user, get_all_users, get_user_by_token, create_user

task_list = UserViewSet.as_view({
    'get': 'me',
    'get': 'getAll',
    'post': 'create',
    'post': 'auth',
})

urlpatterns = [
    path('me', get_user_by_token), 
    path('getAll', get_all_users), 
    path('create', create_user),
    path('auth', auth_user),
]
