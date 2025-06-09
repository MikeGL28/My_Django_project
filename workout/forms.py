# forms.py
from datetime import timedelta
from django import forms
from .models import Training

class TrainingForm(forms.ModelForm):
    class Meta:
        model = Training
        fields = [
            'date', 'description', 'is_completed', 'intensity',
            'pull_ups_max', 'pull_ups_total',
            'dips_max', 'dips_total',
            'push_ups_max', 'push_ups_total',
            'run_distance', 'run_time'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'intensity': forms.HiddenInput(),
            'is_completed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),

            # Подтягивания
            'pull_ups_max': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'placeholder': 'Максимум за подход'}),
            'pull_ups_total': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'placeholder': 'Всего за тренировку'}),

            # Брусья
            'dips_max': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'placeholder': 'Максимум за подход'}),
            'dips_total': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'placeholder': 'Всего за тренировку'}),

            # Отжимания
            'push_ups_max': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'placeholder': 'Максимум за подход'}),
            'push_ups_total': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'placeholder': 'Всего за тренировку'}),

            # Бег
            'run_distance': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'км'}),
            'run_time': forms.TextInput(attrs={'placeholder': 'чч:мм:сс'}),
        }


        def clean_run_time(self):
            data = self.cleaned_data['run_time']
            if data:
                parts = data.split(':')
                if len(parts) == 3:
                    h, m, s = map(int, parts)
                    return timedelta(hours=h, minutes=m, seconds=s)
                elif len(parts) == 2:
                    m, s = map(int, parts)
                    return timedelta(minutes=m, seconds=s)
                else:
                    raise forms.ValidationError("Неверный формат времени. Используйте HH:MM:SS или MM:SS.")
            return None