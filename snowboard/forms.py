from django import forms
from .models import PostSnow

class PostForm(forms.ModelForm):
    class Meta:
        model = PostSnow
        fields = ['title', 'content', 'image', 'address']  # Добавляем поле 'image'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),  # Стилизация поля файла
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите адрес'}),
        }