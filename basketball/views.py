from django.shortcuts import render, redirect, get_object_or_404
from .models import BasketballGame, Player, PlayerGameStats
from .forms import BasketballGameForm, PlayerForm
import calendar
from datetime import datetime


def basketball_profile(request, year=None, month=None):
    now = datetime.now()

    # Получаем текущий или указанный месяц и год
    if year is None:
        year = now.year
    if month is None:
        month = now.month

    games = BasketballGame.objects.filter(date__year=year, date__month=month)
    players = Player.objects.all()

    # Генерация календаря
    calendar_data = get_calendar_data(year, month)

    # Среднее по играм
    total_games = games.count()
    avg_points = round(sum(game.total_points for game in games) / total_games, 2) if total_games else 0

    # Месяцы на русском
    ru_months = {
        1: 'Январь', 2: 'Февраль', 3: 'Март', 4: 'Апрель',
        5: 'Май', 6: 'Июнь', 7: 'Июль', 8: 'Август',
        9: 'Сентябрь', 10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь'
    }
    month_name = ru_months.get(month, 'Неизвестный месяц')

    # Для навигации
    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1

    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1

    return render(request, 'basketball/basketball_profile.html', {
        'games': games,
        'players': players,
        'avg_points': avg_points,
        'calendar': calendar_data,
        'now': now,
        'month_name': month_name,
        'year': year,
        'month': month,
        'prev_month': prev_month,
        'prev_year': prev_year,
        'next_month': next_month,
        'next_year': next_year
    })



def add_player(request):
    if request.method == 'POST':
        form = PlayerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('basketball:basketball_profile')
    else:
        form = PlayerForm()

    return render(request, 'basketball/add_player.html', {'form': form})


def add_basketball_game(request):
    all_players = Player.objects.all()
    if request.method == 'POST':
        form = BasketballGameForm(request.POST)
        if form.is_valid():
            game = form.save()  # Сохраняем игру

            selected_player_ids = request.POST.getlist('players')  # Получаем выбранных игроков
            for player_id in selected_player_ids:
                two = int(request.POST.get(f'two_pointers_{player_id}', 0))
                three = int(request.POST.get(f'three_pointers_{player_id}', 0))

                PlayerGameStats.objects.create(
                    game=game,
                    player_id=player_id,
                    two_pointers=two,
                    three_pointers=three
                )

            return redirect('basketball:basketball_profile')
    else:
        form = BasketballGameForm()

    return render(request, 'basketball/add_basketball_session.html', {
        'form': form,
        'all_players': all_players
    })


def edit_basketball_session(request, pk):
    session = get_object_or_404(BasketballGame, pk=pk)
    if request.method == 'POST':
        form = BasketballGameForm(request.POST, instance=session)
        if form.is_valid():
            form.save()
            return redirect('basketball:basketball_profile')
    else:
        form = BasketballGameForm(instance=session)
    return render(request, 'edit_basketball_session.html', {'form': form})


def get_calendar_data(year, month):
    cal = calendar.Calendar()
    days_in_month = cal.itermonthdays(year, month)

    # Получаем все игры за этот месяц
    games = BasketballGame.objects.filter(date__year=year, date__month=month)
    game_dates = {game.date.day for game in games}

    data = []
    for day in days_in_month:
        if day == 0:
            data.append({'day': '', 'level': 0})  # Пустые дни
        else:
            intensity = 1 if day in game_dates else 0
            data.append({'day': day, 'level': intensity})

    return data


def player_detail(request, pk):
    player = get_object_or_404(Player, pk=pk)
    return render(request, 'basketball/player_detail.html', {'player': player})