from django.contrib import admin
from .models import Training

@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = ('date', 'intensity', 'is_completed')
    list_filter = ('intensity', 'is_completed')