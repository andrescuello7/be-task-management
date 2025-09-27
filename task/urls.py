
from django.urls import path
from task.api import TaskViewSet
from task.views import change_task, delete_task, find_task_by_date, create_task, get_all_tasks

task_list = TaskViewSet.as_view({
    'get': 'getAll',
    'post': 'create',
})

task_detail = TaskViewSet.as_view({
    'get': 'find',
    'put': 'change',
    'delete': 'delete',
})

urlpatterns = [
    path('getAll', get_all_tasks), 
    path('create', create_task),
    path('find', find_task_by_date), 
    path('change', change_task),
    path('delete', delete_task),
]