from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login as auth_login
from django.urls import reverse_lazy
from .models import Task, Category
from .forms import TaskForm, TaskEditForm, RegisterForm


@login_required
def kanban_board(request):
    user = request.user
    tasks = Task.objects.filter(user=user)
    to_do_tasks = tasks.filter(status='to_do')
    in_progress_tasks = tasks.filter(status='in_progress')
    on_review_tasks = tasks.filter(status='on_review')
    done_tasks = tasks.filter(status='done', is_archived=False)
    categories = Category.objects.all()

    if request.method == 'POST':
        form = TaskForm(request.POST)
        category_name = request.POST.get('category_radio')

        if form.is_valid():
            task = form.save(commit=False)
            if category_name == 'personal':
                category, created = Category.objects.get_or_create(name='Личное', defaults={'color': 'blue'})
            elif category_name == 'work':
                category, created = Category.objects.get_or_create(name='Работа', defaults={'color': 'red'})
            else:
                category = None

            task.category = category
            task.user = user
            task.is_priority = 'priority' in request.POST
            task.save()
            form.save_m2m()
            return redirect('kanban:kanban_board')
    else:
        form = TaskForm()

    context = {
        'to_do_tasks': to_do_tasks,
        'in_progress_tasks': in_progress_tasks,
        'on_review_tasks': on_review_tasks,
        'done_tasks': done_tasks,
        'form': form,
        'categories': categories,
    }
    return render(request, 'kanban/kanban_board.html', context)


@csrf_protect
@login_required
def update_task_comment(request, task_id):
    if request.method == 'POST':
        comment = request.POST.get('comment', '').strip()
        task = get_object_or_404(Task, id=task_id, user=request.user)
        task.comment = comment
        task.save()
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


@csrf_protect
@login_required
def update_task_status(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    new_status = request.POST.get('status')
    if new_status in dict(Task.STATUS_CHOICES):
        task.status = new_status
        task.save()
    return redirect('kanban:kanban_board')


@csrf_protect
@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    return redirect('kanban:kanban_board')


@csrf_protect
@login_required
def update_task_category(request, task_id):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        task = get_object_or_404(Task, id=task_id, user=request.user)

        if category_id == 'null':
            task.category = None
        elif category_id:
            category = get_object_or_404(Category, id=category_id)
            task.category = category

        task.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        form = TaskEditForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('kanban:kanban_board')
    else:
        form = TaskEditForm(instance=task)
    return render(request, 'kanban/edit_task.html', {'form': form, 'task': task})


@csrf_protect
@login_required
def archive_task(request, task_id):
    try:
        task = Task.objects.get(id=task_id, user=request.user)
        task.is_archived = True
        task.save()
        return redirect('kanban:kanban_board')
    except Task.DoesNotExist:
        return JsonResponse({'message': 'Задача не найдена'}, status=404)


@login_required
def get_archived_tasks(request):
    tasks = Task.objects.filter(user=request.user, is_archived=True)
    data = [{
        'id': task.id,
        'title': task.title,
        'comment': task.comment or '',
        'category': {'name': task.category.name, 'color': task.category.color} if task.category else None,
    } for task in tasks]
    return JsonResponse(data, safe=False)


@csrf_protect
@login_required
def restore_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.is_archived = False
    task.status = 'to_do'
    task.save()
    return redirect('kanban:kanban_board')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('kanban:kanban_board')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
    return redirect('kanban:kanban_board')

@login_required
def get_task_counts(request):
    user = request.user
    counts = {
        'in_progress': Task.objects.filter(user=user, status='in_progress').count(),
        'on_review': Task.objects.filter(user=user, status='on_review').count(),
        'done': Task.objects.filter(user=user, status='done', is_archived=False).count(),
    }
    return JsonResponse(counts)