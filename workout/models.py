from django.db import models

INTENSITY_CHOICES = [
    (0, 'Нет данных'),
    (1, 'Лёгкая'),
    (2, 'Средняя'),
    (3, 'Хорошая'),
    (4, 'Интенсивная'),
]

class Training(models.Model):
    date = models.DateField(verbose_name='Дата')
    description = models.TextField(blank=True, verbose_name='Описание')
    is_completed = models.BooleanField(default=False, verbose_name='Выполнено')
    intensity = models.PositiveSmallIntegerField(
        choices=INTENSITY_CHOICES,
        default=0,
        verbose_name='Интенсивность'
    )

    # Подтягивания
    pull_ups_max = models.PositiveIntegerField(null=True, blank=True, verbose_name='Подтягивания максимум за подход')
    pull_ups_total = models.PositiveIntegerField(null=True, blank=True, verbose_name='Подтягивания всего за тренировку')

    # Отжимания на брусьях
    dips_max = models.PositiveIntegerField(null=True, blank=True, verbose_name='Брусья максимум за подход')
    dips_total = models.PositiveIntegerField(null=True, blank=True, verbose_name='Брусья всего за тренировку')

    # Отжимания от пола
    push_ups_max = models.PositiveIntegerField(null=True, blank=True, verbose_name='Отжимания максимум за подход')
    push_ups_total = models.PositiveIntegerField(null=True, blank=True, verbose_name='Отжимания всего за тренировку')

    # Бег
    run_distance = models.FloatField(null=True, blank=True, verbose_name='Бег: дистанция (км)')
    run_time = models.DurationField(null=True, blank=True, verbose_name='Время бега')

    def __str__(self):
        return f"Тренировка от {self.date}"

    class Meta:
        verbose_name = 'Тренировка'
        verbose_name_plural = 'Тренировки'