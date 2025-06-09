from django import forms
from .models import GuitarSong

class GuitarSongForm(forms.ModelForm):
    class Meta:
        model = GuitarSong
        fields = ['title', 'artist', 'chords_link']
        labels = {
            'title': 'Название песни',
            'artist': 'Исполнитель',
            'chords_link': 'Ссылка на аккорды',
        }
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Введите название песни'}),
            'artist': forms.TextInput(attrs={'placeholder': 'Введите исполнителя'}),
            'chords_link': forms.URLInput(attrs={'placeholder': 'https://example.com '}),
        }