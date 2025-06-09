from django.contrib import admin
from .models import GuitarSong

@admin.register(GuitarSong)
class GuitarSongAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'chords_link')