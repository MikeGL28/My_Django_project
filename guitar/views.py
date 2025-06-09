from django.shortcuts import render, redirect

from .forms import GuitarSongForm
from .models import GuitarSong

def guitar_page(request):
    songs = GuitarSong.objects.all().order_by('title')
    return render(request, 'guitar/index.html', {'songs': songs})

def add_song(request):
    if request.method == 'POST':
        form = GuitarSongForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('guitar:guitar_page')
    else:
        form = GuitarSongForm()

    return render(request, 'guitar/add_song.html', {'form': form})