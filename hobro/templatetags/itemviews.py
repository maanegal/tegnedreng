from datetime import datetime
from ..models import *
from hobro.helpers import get_current_info
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
    return {'song': song.first()}


@register.inclusion_tag('hobro/embed_album.html')
def embed_album(album):
    return {'album': album.first()}


@register.inclusion_tag('hobro/embed_musicvideo.html')
def embed_musicvideo(musicvideo):
    return {'musicvideo': musicvideo.first()}


@register.inclusion_tag('hobro/embed_character.html')
def embed_character(character):
    return {'character': character.first()}
