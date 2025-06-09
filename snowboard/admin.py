from django.contrib import admin
from .models import PostSnow


@admin.register(PostSnow)
class PostAdminSnow(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'published_at')


