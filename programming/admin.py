from django.contrib import admin
from .models import Certificate, TelegramPost

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title',)

@admin.register(TelegramPost)
class TelegramPostAdmin(admin.ModelAdmin):
    list_display = ('text', 'image', 'created_at')

