from django.urls import path
from . import views

app_name = 'basketball'

urlpatterns = [
    path('', views.basketball_profile, name='basketball_profile'),
    path('game/add/', views.add_basketball_game, name='add_basketball_game'),
    path('game/edit/<int:pk>/', views.edit_basketball_session, name='edit_basketball_session'),
    path('player/add/', views.add_player, name='add_player'),
    path('player/<int:pk>/', views.player_detail, name='player_detail'),
    path('<int:year>/<int:month>/', views.basketball_profile, name='basketball_profile_with_date'),
]