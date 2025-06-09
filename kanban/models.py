from django.db import models
from django.conf import settings


class Tag(models.Model):
    name = models.CharField('Название тега', max_length=50, unique=True)
    color = models.CharField('Цвет (HEX или название)', max_length=50, default='gray')
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField('Название категории', max_length=100)
    color = models.CharField('Цвет (HEX или название)', max_length=50, default='gray')
    def __str__(self):
        return self.name

class Task(models.Model):
    STATUS_CHOICES = (
        ('to_do', 'Задача'),
        ('in_progress', 'В работе'),
        ('on_review', 'На проверке'),
        ('done', 'Выполнено'),
    )
    title = models.CharField('Задача', max_length=255)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='to_do')
    tags = models.ManyToManyField('Tag', blank=True, verbose_name='Теги')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Категория')
    comment = models.TextField('Комментарий', blank=True, null=True)  # Новое поле
    created_at = models.DateTimeField(auto_now_add=True)
    is_archived = models.BooleanField(default=False, verbose_name='В архиве')
    is_priority = models.BooleanField(default=False, verbose_name='Приоритетная')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    def __str__(self):
        return self.title