from django.shortcuts import render, get_object_or_404
from .models import *
from .helpers import the_big_retriever, class_from_str, make_bandcamp_embed, make_spotify_embed, make_youtube_embed


def item_list(request, index=0):
    data = the_big_retriever(index)
    return render(request, 'hobro/item_list.html', {'items': data})


def item_detail(request, pk, tp):
    cl = class_from_str(tp)
    item = get_object_or_404(cl, pk=pk)
    return render(request, 'hobro/item_detail.html', {'item': item})


def song_viewer(request, pk):
    song = get_object_or_404(Song, pk=pk)
    a = None
    if song.album:
        a = song.album
    embed_bc = make_bandcamp_embed(album=a, song=song)
    embed_sp = make_spotify_embed(album=None, song=song)
    return render(request, 'hobro/song_viewer.html', {'song': song, 'embed_code_bc': embed_bc, 'embed_code_sp': embed_sp})


def album_viewer(request, pk):
    album = get_object_or_404(Album, pk=pk)
    embed_bc = make_bandcamp_embed(album=album, song=None)
    embed_sp = make_spotify_embed(album=album, song=None)
    return render(request, 'hobro/album_viewer.html', {'album': album, 'embed_code_bc': embed_bc, 'embed_code_sp': embed_sp})


def musicvideo_viewer(request, pk):
    musicvideo = get_object_or_404(MusicVideo, pk=pk)
    embed = make_youtube_embed(musicvideo)
    return render(request, 'hobro/musicvideo_viewer.html', {'musicvideo': musicvideo, 'embed_code': embed})


def music_list(request):
    albums = Album.objects.all()
    songs = Song.objects.all().order_by('title')
    musicvideos = MusicVideo.objects.all().order_by('title')
    characters = Character.objects.all().order_by('name')
    return render(request, 'hobro/music_list.html', {'albums': albums, 'songs': songs, 'musicvideos': musicvideos,
                                                     'characters': characters})


def character_viewer(request, pk):
    character = get_object_or_404(Character, pk=pk)
    posts = list(character.post_set.all()) + list(character.postphoto_set.all()) + list(character.postvideo_set.all())
    return render(request, 'hobro/character_viewer.html', {'character': character, 'posts': posts})


def hashtag_viewer(request, pk):
    hashtag = get_object_or_404(Hashtag, pk=pk)
    print(pk, 'got this', hashtag.name)
    return render(request, 'hobro/hashtag_viewer.html', {'hashtag': hashtag})
