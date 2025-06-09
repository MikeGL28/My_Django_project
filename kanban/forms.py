from django import forms
from .models import Task, Category, Tag
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class TaskForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control', 'id': 'task-tags'}),
        label='Теги'
    )

    class Meta:
        model = Task
        fields = ['title', 'category', 'tags', 'comment']  # ← добавлено
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название задачи'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Введите комментарий'}),  # ← добавлено
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()
        self.fields['category'].empty_label = "Без категории"


class TaskEditForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'category', 'tags', 'comment']  # ← добавлено
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control', 'id': 'task-tags'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),  # ← добавлено
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()
        self.fields['category'].empty_label = "Без категории"
        self.fields['tags'].queryset = Tag.objects.all()


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]