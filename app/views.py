from django.shortcuts import render, get_object_or_404, redirect
from .models import Song
from .utils import parse_chordspro
from .forms import SongForm

# Create your views here.

def index(request):
    songs = Song.objects.all()
    return render(request, 'index.html', {
        'songs': songs
    })

def song(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    chart = parse_chordspro(song.chordspro)
    return render(request, "song.html", {
        "chart": chart
    })

def upload_song(request):
    if request.method == 'POST': 
        form = SongForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')
    else: 
        form = SongForm()

    return render(request, 'upload_song.html', {
        'form': form
    })