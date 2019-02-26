from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .helpers import the_big_retriever, class_from_str, make_bandcamp_embed, make_spotify_embed, make_youtube_embed


def frontpage(request):
    return render(request, 'hobro/frontpage.html')


def item_list(request):
    data = the_big_retriever()
    comment_pref = request.COOKIES['show_comments']
    return render(request, 'hobro/item_list.html', {'items': data, 'comment_pref': comment_pref})


def item_page(request, number=1):
    data = the_big_retriever(number)
    next_page = None
    if not number == 8:
        next_page = number + 1
    comment_pref = request.COOKIES['show_comments']
    return render(request, 'hobro/item_list.html', {'items': data, 'next': next_page, 'comment_pref': comment_pref})


def item_detail(request, pk, tp):
    cl = class_from_str(tp)
    item = get_object_or_404(cl, pk=pk)
    return render(request, 'hobro/item_detail.html', {'item': item})


def song_viewer(request, slug):
    song = get_object_or_404(Song, slug=slug)
    a = None
    if song.album:
        a = song.album
    embed_bc = make_bandcamp_embed(album=a, song=song)
    embed_sp = make_spotify_embed(album=None, song=song)
    return render(request, 'hobro/song_viewer.html', {'song': song, 'embed_code_bc': embed_bc, 'embed_code_sp': embed_sp})


def album_viewer(request, slug):
    album = get_object_or_404(Album, slug=slug)
    embed_bc = make_bandcamp_embed(album=album, song=None)
    embed_sp = make_spotify_embed(album=album, song=None)
    return render(request, 'hobro/album_viewer.html', {'album': album, 'embed_code_bc': embed_bc, 'embed_code_sp': embed_sp})


def musicvideo_viewer(request, slug):
    musicvideo = get_object_or_404(MusicVideo, slug=slug)
    embed = make_youtube_embed(musicvideo)
    return render(request, 'hobro/musicvideo_viewer.html', {'musicvideo': musicvideo, 'embed_code': embed})


def music_list(request):
    albums = Album.objects.order_by('release_date')
    songs = Song.objects.order_by('title')
    musicvideos = MusicVideo.objects.order_by('title')
    characters = Character.objects.order_by('name')
    return render(request, 'hobro/music_list.html', {'albums': albums, 'songs': songs, 'musicvideos': musicvideos,
                                                     'characters': characters})


def character_list(request):
    characters = Character.objects.order_by('?')
    return render(request, 'hobro/character_list.html', {'characters': characters})


def character_viewer(request, slug):
    character = get_object_or_404(Character, slug=slug)
    posts = list(character.post_set.all()) + list(character.postphoto_set.all()) + list(character.postvideo_set.all())
    return render(request, 'hobro/character_viewer.html', {'character': character, 'posts': posts})


def hashtag_list(request):
    hashtags = Hashtag.objects.order_by('name')
    return render(request, 'hobro/hashtag_list.html', {'hashtags': hashtags})


def hashtag_viewer(request, slug):
    hashtag = get_object_or_404(Hashtag, slug=slug)
    return render(request, 'hobro/hashtag_viewer.html', {'hashtag': hashtag})


# REDIRECTS
def redirect_music(request):
    response = redirect('/musik/')
    return response


def redirect_chapter(request):
    response = redirect('/kapitel/1/')
    return response


def redirect_character(request):
    response = redirect('/medlemmer/')
    return response


def redirect_hashtag(request):
    response = redirect('/hashtags/')
    return response
