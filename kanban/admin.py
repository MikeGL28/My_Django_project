from django.contrib import admin
from .models import Task, Category

class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'category', 'is_archived']
    list_filter = ['status', 'category', 'is_archived']
    search_fields = ['title', 'comment']

admin.site.register(Task)
admin.site.register(Category)