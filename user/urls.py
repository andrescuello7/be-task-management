from django.urls import path
from user.api import UserViewSet
from user.views import auth_user, get_all_users, get_user_by_token, create_user

task_list = UserViewSet.as_view({
    'get': 'getAll',
    'post': 'create',
})

task_detail = UserViewSet.as_view({
    'get': 'me',
    'post': 'auth',
})

urlpatterns = [
    path('getAll', get_all_users), 
    path('create', create_user),
    path('me', get_user_by_token), 
    path('auth', auth_user),
]
