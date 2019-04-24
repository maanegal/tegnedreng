from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .helpers import the_big_retriever, class_from_str, make_bandcamp_embed, make_spotify_embed, make_youtube_embed
from django.db.models import Q
from itertools import chain
from random import shuffle


def frontpage(request):
    return render(request, 'hobro/frontpage.html')


def about(request):
    return render(request, 'hobro/about.html')


def search_index(request):
    query = request.GET.get('q')
    q_song = Q(title__icontains=query) | Q(lyrics__icontains=query) | Q(text__icontains=query)
    q_post = Q(text__icontains=query)
    q_media = Q(title__icontains=query) | Q(text__icontains=query)
    q_char = Q(name__icontains=query) | Q(text__icontains=query)
    if query:
        results = list(chain(Character.objects.filter(q_char).distinct(),
                        Album.objects.filter(q_media).distinct(),
                        MusicVideo.objects.filter(q_media).distinct(),
                        Song.objects.filter(q_song).distinct(),
                        Post.objects.filter(q_post).distinct(),
                        PostPhoto.objects.filter(q_post).distinct(),
                        PostVideo.objects.filter(q_post).distinct(),
                        SwgrsPost.objects.filter(q_post).distinct(),
                        SwgrsMedia.objects.filter(q_post).distinct(),
                        SwgrsSong.objects.filter(q_media).distinct()
                        ))
    else:
        results = []
    return render(request, 'hobro/search_index.html', {'query': query, 'results': results})


def item_page(request, number=1):
    previous_page = request.META.get('HTTP_REFERER')
    p = "/kapitel/"+str(number - 1)
    if previous_page and p in previous_page:
        continued = True
    else:
        continued = False
    data = the_big_retriever(number)
    next_page = None
    if not number == 8:
        next_page = number + 1
    comment_pref = request.COOKIES.get('show_comments')
    return render(request, 'hobro/item_list.html', {'items': data, 'number': number, 'next': next_page, 'comment_pref': comment_pref, 'continued': continued})


def item_detail(request, slug, tp):
    cl = class_from_str(tp)
    item = get_object_or_404(cl, slug=slug)
    comment_pref = request.COOKIES.get('show_comments')
    return render(request, 'hobro/item_detail.html', {'item': item, 'comment_pref': comment_pref})


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
    swgrs = SwgrsSong.objects.order_by('title')
    musicvideos = MusicVideo.objects.order_by('title')
    characters = Character.objects.order_by('name')
    return render(request, 'hobro/music_list.html', {'albums': albums, 'songs': songs, 'musicvideos': musicvideos,
                                                     'characters': characters, 'swgrs': swgrs})


def character_list(request):
    characters = Character.objects.order_by('?')
    return render(request, 'hobro/character_list.html', {'characters': characters})


def character_viewer(request, slug):
    character = get_object_or_404(Character, slug=slug)
    posts = list(character.post_set.all()) + list(character.postphoto_set.all()) + list(character.postvideo_set.all()) \
        + list(character.swgrspost_set.all()) + list(character.swgrsmedia_set.all())
    return render(request, 'hobro/character_viewer.html', {'character': character, 'posts': posts})


def hashtag_list(request):
    hashtags = Hashtag.objects.order_by('name')
    return render(request, 'hobro/hashtag_list.html', {'hashtags': hashtags})


def hashtag_viewer(request, slug):
    hashtag = get_object_or_404(Hashtag, slug=slug)
    return render(request, 'hobro/hashtag_viewer.html', {'hashtag': hashtag})


def photo_gallery(request):
    objects = []
    objects.extend(list(PostPhoto.objects.order_by('?')[:16]))
    objects.extend(list(SwgrsMedia.objects.order_by('?')[:4]))
    shuffle(objects)
    return render(request, 'hobro/photo_gallery.html', {'objects': objects})



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


# Error Pages

def handler500(request):
    return render(request, 'errors/500.html')


def handler404(request, exception):
    return render(request, 'errors/404.html')


def handler403(request, exception):
    return render(request, 'errors/403.html')


def handler400(request, exception):
    return render(request, 'errors/400.html')

