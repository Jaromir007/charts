from django.urls import path 
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('song/<int:song_id>/', views.song, name='song'),
    path('upload_song', views.upload_song, name='upload_song')
]