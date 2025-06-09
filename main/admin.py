from django.contrib import admin

from .models import PostView, Category



class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'published', 'category_hobby')


admin.site.register(PostView, PostAdmin)
admin.site.register(Category)
