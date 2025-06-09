from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'kanban'

urlpatterns = [
    path('', views.kanban_board, name='kanban_board'),
    path('update-task/<int:task_id>/', views.update_task_status, name='update_task_status'),
    path('delete-task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('edit-task/<int:task_id>/', views.edit_task, name='edit_task'),
    path('update-category/<int:task_id>/', views.update_task_category, name='update_task_category'),
    path('update-task-comment/<int:task_id>/', views.update_task_comment, name='update_task_comment'),
    path('task/<int:task_id>/archive/', views.archive_task, name='archive_task'),
    path('archived-tasks/', views.get_archived_tasks, name='get_archived_tasks'),
    path('task/<int:task_id>/restore/', views.restore_task, name='restore_task'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('task-counts/', views.get_task_counts, name='task_counts'),
]
