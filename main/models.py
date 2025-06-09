from django.db import models


class PostView(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название поста")
    content = models.TextField(verbose_name="Содержание поста")
    published = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")
    category_hobby = models.ForeignKey('Category', null=True, on_delete=models.PROTECT, verbose_name="Категория хобби")

    class Meta:
        verbose_name_plural = 'Посты'
        verbose_name = 'Пост'


class Category(models.Model):
    name = models.CharField(max_length=20, verbose_name="Название")
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Категорий'
        verbose_name = 'категорию'