# todo/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm

@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user).exclude(status='F')
    return render(request, 'todo/task_list.html', {'tasks': tasks})

@login_required
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('todo:task_list')
    else:
        form = TaskForm()
    return render(request, 'todo/add_task.html', {'form': form})

@login_required
def update_task_status(request, task_id, status):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.status = status
    task.save()
    return redirect('todo:task_list')

@login_required
def uncompleted_tasks(request):
    tasks = Task.objects.filter(user=request.user, status='U')
    return render(request, 'todo/task_list.html', {'tasks': tasks})

@login_required
def in_progress_tasks(request):
    tasks = Task.objects.filter(user=request.user, status='P')
    return render(request, 'todo/task_list.html', {'tasks': tasks})

@login_required
def completed_tasks(request):
    tasks = Task.objects.filter(user=request.user, status='F')
    return render(request, 'todo/task_list.html', {'tasks': tasks})
