from django.shortcuts import render, get_object_or_404
from .models import *
from .helpers import the_big_retriever


def item_list(request):
    data = the_big_retriever()
    return render(request, 'hobro/item_list.html', {'items': data})


def item_detail(request, pk):
    item = get_object_or_404(Section, pk=pk)
    return render(request, 'hobro/item_detail.html', {'item': item})


def song_viewer(request, pk):
    song = get_object_or_404(Song, pk=pk)
    return render(request, 'hobro/song_viewer.html', {'song': song})


def album_viewer(request, pk):
    album = get_object_or_404(Album, pk=pk)
    return render(request, 'hobro/album_viewer.html', {'album': album})


def music_list(request):
    albums = Album.objects.all()
    songs = Song.objects.all().order_by('title')
    characters = Character.objects.all().order_by('name')
    return render(request, 'hobro/music_list.html', {'albums': albums, 'songs': songs, 'characters': characters})


def character_viewer(request, pk):
    character = get_object_or_404(Character, pk=pk)
    posts = list(character.post_set.all()) + list(character.postphoto_set.all()) + list(character.postvideo_set.all())
    return render(request, 'hobro/character_viewer.html', {'character': character, 'posts': posts})
