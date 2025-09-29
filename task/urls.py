
from django.urls import path
from task.api import TaskViewSet
from task.views import change_task, delete_task, find_task_by_date, create_task, get_all_tasks, get_filter_search

task_list = TaskViewSet.as_view({
    'post': 'create',
    'get': 'find',
    'get': 'search',
    'get': 'getAll',
    'put': 'change',
    'delete': 'delete',
})

urlpatterns = [
    path('getAll/', get_all_tasks), 
    path('create/', create_task),
    path('find/', find_task_by_date), 
    path('search/', get_filter_search), 
    path('change/', change_task),
    path('delete/', delete_task),
]