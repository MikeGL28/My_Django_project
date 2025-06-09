from django import forms
from .models import BasketballGame, Player, PlayerGameStats

class BasketballGameForm(forms.ModelForm):
    players = forms.ModelMultipleChoiceField(
        queryset=Player.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label='Игроки'
    )

    class Meta:
        model = BasketballGame
        fields = ['date', 'two_pointers', 'three_pointers']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'date': 'Введите дату',
            'two_pointers': '2-очковые броски (общие)',
            'three_pointers': '3-очковые броски (общие)',
        }

class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = [
            'full_name',
            'position',
            'jersey_number',
            'height',
            'weight',
            'two_pointers',
            'three_pointers',
            'photo'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Введите ФИО'}),
            'position': forms.TextInput(attrs={'placeholder': 'Например: защитник'}),
        }
        labels = {
            'full_name': 'ФИО',
            'position': 'Позиция',
            'jersey_number': 'Номер на майке',
            'height': 'Рост (см)',
            'weight': 'Вес (кг)',
            'two_pointers': '2-очковые броски',
            'three_pointers': '3-очковые броски',
            'photo': 'Фото игрока',
        }