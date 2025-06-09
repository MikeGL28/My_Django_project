from django.db import models

class Player(models.Model):
    full_name = models.CharField("ФИО", max_length=100)
    position = models.CharField("Позиция", max_length=50)
    two_pointers = models.PositiveIntegerField("2-очковые", default=0)
    three_pointers = models.PositiveIntegerField("3-очковые", default=0)
    total_points = models.PositiveIntegerField("Общее количество очков", default=0, blank=True)
    avg_points = models.FloatField("Средние очки за игру", default=0, blank=True)
    weight = models.PositiveIntegerField("Вес (кг)", blank=True, null=True)
    height = models.PositiveIntegerField("Рост (см)", blank=True, null=True)
    jersey_number = models.PositiveIntegerField("Номер на майке", blank=True, null=True)
    photo = models.ImageField("Фото игрока", upload_to='basketball/players/', blank=True, null=True)

    def calculate_total_points(self):
        return self.two_pointers * 2 + self.three_pointers * 3

    def save(self, *args, **kwargs):
        # Автоматический расчёт
        self.total_points = self.calculate_total_points()
        games_played = BasketballGame.objects.count()  # Пример количества игр
        if games_played > 0:
            self.avg_points = self.total_points / games_played
        else:
            self.avg_points = 0.0
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name

INTENSITY_CHOICES = [
    (0, 'Нет данных'),
    (1, 'Мало активности'),
    (2, 'Средняя активность'),
    (3, 'Хорошая тренировка'),
    (4, 'Отличная тренировка'),
]

class BasketballGame(models.Model):
    date = models.DateField()  # Убран auto_now_add
    two_pointers = models.PositiveIntegerField("2-очковые", default=0)
    three_pointers = models.PositiveIntegerField("3-очковые", default=0)
    total_points = models.PositiveIntegerField("Общее число очков", default=0)

    def save(self, *args, **kwargs):
        self.total_points = self.two_pointers * 2 + self.three_pointers * 3
        super().save(*args, **kwargs)


class PlayerGameStats(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    game = models.ForeignKey(BasketballGame, on_delete=models.CASCADE)
    two_pointers = models.PositiveIntegerField(default=0)
    three_pointers = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Обновляем общую статистику игрока
        stats = self.player.playergamestats_set.aggregate(
            total_two=models.Sum('two_pointers'),
            total_three=models.Sum('three_pointers')
        )

        self.player.two_pointers = stats['total_two'] or 0
        self.player.three_pointers = stats['total_three'] or 0
        self.player.total_points = self.player.calculate_total_points()

        games_played = self.player.playergamestats_set.values('game').distinct().count()
        self.player.avg_points = self.player.total_points / games_played if games_played else 0

        self.player.save()

    def __str__(self):
        return f"{self.player} - {self.game}"