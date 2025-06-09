from django.db import models
from django.utils import timezone

class PostSnow(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок поста')
    content = models.TextField(verbose_name='Текст поста')
    image = models.ImageField(upload_to='snowboard_images/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Время создания поста')
    published_at = models.DateTimeField(blank=True, null=True, verbose_name='Время публикации поста')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    def publish(self):
        self.published_at = timezone.now()
        self.save()

    def __str__(self):
        return self.title
