from datetime import datetime
from ..models import *
from hobro.helpers import get_current_info, make_bandcamp_embed, make_spotify_embed, make_youtube_embed
from django import template
register = template.Library()


@register.inclusion_tag('hobro/post.html')
def show_post(post):
    info = get_current_info(post.time_stamp)
    dt = datetime.utcfromtimestamp(post.time_stamp)
    return {'post': post, 'name': info.get('name', ''), 'profilepic': info.get('photo', ''), 'post_time': dt}


@register.inclusion_tag('hobro/postphoto.html')
def show_postphoto(postphoto):
    info = get_current_info(postphoto.time_stamp)
    dt = datetime.utcfromtimestamp(postphoto.time_stamp)
    return {'post': postphoto, 'name': info.get('name', ''), 'profilepic': info.get('photo', ''), 'post_time': dt}


@register.inclusion_tag('hobro/postvideo.html')
def show_postvideo(postvideo):
    info = get_current_info(postvideo.time_stamp)
    dt = datetime.utcfromtimestamp(postvideo.time_stamp)
    return {'post': postvideo, 'name': info.get('name', ''), 'profilepic': info.get('photo', ''), 'post_time': dt}


@register.inclusion_tag('hobro/section.html')
def show_section(section):
    return {'section': section}


@register.inclusion_tag('hobro/story.html')
def show_story(story):
    return {'story': story}


@register.inclusion_tag('hobro/profileevent.html')
def show_profileevent(profileevent):
    dt = datetime.utcfromtimestamp(profileevent.time_stamp)
    return {'profileevent': profileevent, 'post_time': dt}


@register.inclusion_tag('hobro/itemembed.html')
def show_itemembed(itemembed):
    dt = datetime.utcfromtimestamp(itemembed.time_stamp)
    kind = itemembed.what_kind()
    return {'itemembed': itemembed, 'post_time': dt, 'kind': kind}


@register.inclusion_tag('hobro/embed_song.html')
def embed_song(song):
    s = song.first()
    a = None
    if s.album:
        a = s.album
    embed_bc = make_bandcamp_embed(a, s)
    embed_sp = make_spotify_embed(s)
    return {'song': s, 'embed-code-bc': embed_bc, 'embed-code-sp': embed_sp}


@register.inclusion_tag('hobro/embed_album.html')
def embed_album(album):
    embed_bc = make_bandcamp_embed(album.first())
    embed_sp = make_spotify_embed(album.first())
    return {'album': album.first(), 'embed-code-bc': embed_bc, 'embed-code-sp': embed_sp}


@register.inclusion_tag('hobro/embed_musicvideo.html')
def embed_musicvideo(musicvideo):
    embed = make_youtube_embed(musicvideo.first())
    return {'musicvideo': musicvideo.first(), 'embed-code': embed}


@register.inclusion_tag('hobro/embed_character.html')
def embed_character(character):
    return {'character': character.first()}
