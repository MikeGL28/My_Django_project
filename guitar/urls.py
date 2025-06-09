from django.urls import path
from . import views

app_name = 'guitar'

urlpatterns = [
    path('', views.guitar_page, name='guitar_page'),
    path('add_song/', views.add_song, name='add_song')
]