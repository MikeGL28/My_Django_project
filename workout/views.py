from django.shortcuts import render, redirect, get_object_or_404
from .models import Training
from .forms import TrainingForm
import pandas as pd
import plotly.express as px
import plotly.io as pio
import calendar
from datetime import datetime


def generate_gradient_chart(title, y_label, data, y_col='Значение', custom_hover=None, color='#08F7FE'):
    if not data or len(data) == 0:
        return None

    df = pd.DataFrame(data)

    # Проверяем наличие поля "Общее количество"
    has_total = 'Общее количество' in df.columns

    fig = px.line(
        df,
        x='Дата',
        y=y_col,
        title=title,
        hover_data=['Общее количество'] if has_total else None
    )

    fig.update_layout(
        title=dict(text=title, x=0.5, font=dict(size=18, color="#FFFFFF")),
        xaxis_title=None,
        yaxis_title=y_label,
        template="plotly_dark",
        paper_bgcolor='rgba(30, 30, 30, 0.95)',
        plot_bgcolor='rgba(20, 20, 20, 1)',
        font=dict(family="Arial", size=12, color="#FFFFFF"),
        margin=dict(l=60, r=30, t=50, b=20),
        showlegend=False,
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            ticks='',
            ticklen=0
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(60, 60, 60, 0.5)',
            zeroline=False,
            showticklabels=True,
            ticks='outside',
            ticklen=5
        )
    )

    fig.update_traces(
        line=dict(color=color, width=3, shape='spline'),
        fill='tozeroy',
        fillcolor=f'rgba({int(color[1:3], 16)}, {int(color[3:5], 16)}, {int(color[5:7], 16)}, 0.1)',
        mode='lines+markers',
        marker=dict(size=6, color=color),
        hovertemplate=
        "<b>Дата:</b> %{x|%d.%m.%Y}<br>" +
        f"<b>{y_label}</b>: %{{y}}<br>" +
        (f"<b>Общее количество:</b> %{{customdata[0]}}<br><extra></extra>" if has_total else "<extra></extra>"),
        customdata=df[['Общее количество']].values if has_total else None
    )

    return pio.to_html(fig, full_html=False, include_plotlyjs=True)

def decimal_minutes_to_mmss(decimal_minutes):
    minutes = int(decimal_minutes)
    seconds = int(round((decimal_minutes - minutes) * 60))
    if seconds >= 60:
        minutes += 1
        seconds = 0
    return f"{minutes}:{seconds:02d}"

def training_list(request):
    trainings = Training.objects.all().order_by('date')

    # === Сбор данных для графиков ===
    pull_ups_data = []
    dips_data = []
    push_ups_data = []
    run_data = []

    for t in trainings:
        if t.pull_ups_max:
            pull_ups_data.append({
                'Дата': t.date,
                'Значение': t.pull_ups_max,
                'Общее количество': t.pull_ups_total or 0
            })

        # Брусья
        if t.dips_max:
            dips_data.append({
                'Дата': t.date,
                'Значение': t.dips_max,
                'Общее количество': t.dips_total or 0
            })

        if t.push_ups_max:
            push_ups_data.append({
                'Дата': t.date,
                'Значение': t.push_ups_max,
                'Общее количество': t.push_ups_total or 0
            })

        # Бег
        if t.run_distance and t.run_time:
            total_seconds = t.run_time.total_seconds()
            total_minutes = total_seconds / 60
            try:
                pace_decimal = round(total_minutes / t.run_distance, 2)
                pace_str = decimal_minutes_to_mmss(pace_decimal)
                run_data.append({
                    'Дата': t.date,
                    'Значение': pace_decimal,
                    'Дистанция': t.run_distance,
                    'Время': str(t.run_time),  # или форматированная строка
                    'Темп (мин/км)': pace_str
                })
            except ZeroDivisionError:
                pass

    # === Генерация графиков через Plotly ===
    pull_ups_chart = generate_gradient_chart(
        "🏋️ Подтягивания",
        "Количество (max за подход)",
        pull_ups_data,
        y_col='Значение',
        custom_hover=['Общее количество'],
        color="#cc0000"
    ) if pull_ups_data else None

    dips_chart = generate_gradient_chart(
        "🪵 Брусья",
        "Количество (max за подход)",
        dips_data,
        y_col='Значение',
        custom_hover=['Общее количество'],
        color="#cc0000"
    ) if dips_data else None

    push_ups_chart = generate_gradient_chart(
        "🖐️ Отжимания",
        "Количество (max за подход)",
        push_ups_data,
        y_col='Значение',
        custom_hover=['Общее количество'],
        color="#cc0000"
    ) if push_ups_data else None

    run_chart = generate_gradient_chart(
        "🏃‍♂️ Темп бега",
        "Темп (мин/км)",
        run_data,
        y_col='Значение',
        custom_hover=['Дистанция', 'Темп (мин:сек)'],
        color="#cc0000"
    ) if run_data else None

    # === Календарь тренировок ===
    now = datetime.now()
    current_year = now.year
    current_month = now.month

    _, days_in_month = calendar.monthrange(current_year, current_month)

    training_dict = {}
    for t in trainings:
        if t.date.year == current_year and t.date.month == current_month:
            training_dict[t.date.day] = t.intensity

    calendar_days = [
        {'day': day, 'level': training_dict.get(day, 0)}
        for day in range(1, days_in_month + 1)
    ]

    context = {
        'pull_ups_chart': pull_ups_chart,
        'dips_chart': dips_chart,
        'push_ups_chart': push_ups_chart,
        'run_chart': run_chart,

        'calendar': calendar_days,
        'month_name': now.strftime('%B'),
        'now': now
    }

    return render(request, 'training_list.html', context)


def add_training(request):
    if request.method == 'POST':
        form = TrainingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('workout:training_list')
    else:
        form = TrainingForm()

    return render(request, 'add_training.html', {'form': form})


def edit_training(request, pk):
    training = get_object_or_404(Training, pk=pk)
    if request.method == 'POST':
        form = TrainingForm(request.POST, instance=training)
        if form.is_valid():
            form.save()
            return redirect('workout:training_list')
    else:
        form = TrainingForm(instance=training)
    return render(request, 'edit_training.html', {'form': form})

