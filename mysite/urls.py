"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from kanban import views as kanban_views  # <<< Добавлен импорт

urlpatterns = [
    path('admin/', admin.site.urls),

    # Приложения
    path('', include('main.urls', namespace='home')),
    path('programming/', include('programming.urls', namespace='programming')),
    path('snowboarding/', include('snowboard.urls', namespace='snowboarding')),
    path('basketball/', include('basketball.urls', namespace='basketball')),
    path('guitar/', include('guitar.urls', namespace='guitar')),
    path('workout/', include('workout.urls', namespace='workout')),
    path('kanban/', include('kanban.urls', namespace='kanban')),

    # Аутентификация
    path('accounts/', include('django.contrib.auth.urls')),  # Сначала подключаем стандартные URL аутентификации
    path('accounts/profile/', kanban_views.profile, name='profile'),  # <<< После этого добавляем свой маршрут
]

# Подключение медиа-файлов (только в режиме разработки)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)