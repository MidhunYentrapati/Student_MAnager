# todo/urls.py
from django.urls import path
from . import views

app_name = 'todo'

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('add/', views.add_task, name='add_task'),
    path('update_status/<int:task_id>/<str:status>/', views.update_task_status, name='update_task_status'),
    path('uncompleted/', views.uncompleted_tasks, name='uncompleted_tasks'),
    path('in_progress/', views.in_progress_tasks, name='in_progress_tasks'),
    path('completed/', views.completed_tasks, name='completed_tasks'),
]
