from django.db import models

class GuitarSong(models.Model):
    title = models.CharField("Название песни", max_length=100)
    artist = models.CharField("Исполнитель", max_length=100)
    chords_link = models.URLField("Ссылка на аккорды")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.artist} - {self.title}"