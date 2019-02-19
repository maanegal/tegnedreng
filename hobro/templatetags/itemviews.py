from datetime import datetime
from ..models import *
from hobro.helpers import get_current_info, make_bandcamp_embed, make_spotify_embed, make_youtube_embed, \
    make_soundcloud_embed, get_layout
from django import template
register = template.Library()


@register.inclusion_tag('hobro/post.html')
def show_post(post):
    info = get_current_info(post.time_stamp)
    dt = datetime.fromtimestamp(post.time_stamp)
    outer, inner = get_layout(post.layout)
    return {'post': post, 'name': info.get('name', ''), 'profilepic': info.get('photo', ''), 'post_time': dt,
            'layout_outer': outer, 'layout_inner': inner}


@register.inclusion_tag('hobro/postphoto.html')
def show_postphoto(postphoto):
    info = get_current_info(postphoto.time_stamp)
    dt = datetime.fromtimestamp(postphoto.time_stamp)
    return {'post': postphoto, 'name': info.get('name', ''), 'profilepic': info.get('photo', ''), 'post_time': dt}


@register.inclusion_tag('hobro/postvideo.html')
def show_postvideo(postvideo):
    info = get_current_info(postvideo.time_stamp)
    dt = datetime.fromtimestamp(postvideo.time_stamp)
    return {'post': postvideo, 'name': info.get('name', ''), 'profilepic': info.get('photo', ''), 'post_time': dt}


@register.inclusion_tag('hobro/section.html')
def show_section(section):
    return {'section': section}


@register.inclusion_tag('hobro/story.html')
def show_story(story):
    return {'story': story}


@register.inclusion_tag('hobro/profileevent.html')
def show_profileevent(profileevent):
    dt = datetime.fromtimestamp(profileevent.time_stamp)
    return {'profileevent': profileevent, 'post_time': dt}


@register.inclusion_tag('hobro/itemembed.html')
def show_itemembed(itemembed):
    dt = datetime.fromtimestamp(itemembed.time_stamp)
    kind = itemembed.what_kind()
    return {'itemembed': itemembed, 'post_time': dt, 'kind': kind}


@register.inclusion_tag('hobro/embed_song.html')
def embed_song(song):
    s = song.first()
    a = None
    if s.album:
        a = s.album
    embed_bc = make_bandcamp_embed(album=a, song=s)
    embed_sp = make_spotify_embed(album=None, song=s)
    return {'song': s, 'embed_code_bc': embed_bc, 'embed_code_sp': embed_sp}


@register.inclusion_tag('hobro/embed_album.html')
def embed_album(album):
    al = album.first()
    embed_bc = make_bandcamp_embed(album=al, song=None)
    embed_sp = make_spotify_embed(album=al, song=None)
    return {'album': al, 'embed_code_bc': embed_bc, 'embed_code_sp': embed_sp}


@register.inclusion_tag('hobro/embed_musicvideo.html')
def embed_musicvideo(musicvideo):
    embed = make_youtube_embed(musicvideo.first())
    return {'musicvideo': musicvideo.first(), 'embed_code': embed}


@register.inclusion_tag('hobro/embed_character.html')
def embed_character(character):
    return {'character': character.first()}


@register.inclusion_tag('hobro/swgrspost.html')
def show_swgrspost(swgrspost):
    dt = datetime.fromtimestamp(swgrspost.time_stamp)
    outer, inner = get_layout(swgrspost.layout)
    yt = ""
    if swgrspost.link_yt:
        yt = make_youtube_embed(swgrspost)
    return {'swgrspost': swgrspost, 'post_time': dt, 'yt_embed': yt, 'layout_outer': outer, 'layout_inner': inner}


@register.inclusion_tag('hobro/swgrsmedia.html')
def show_swgrsmedia(swgrsmedia):
    dt = datetime.fromtimestamp(swgrsmedia.time_stamp)
    if swgrsmedia.video:
        video = swgrsmedia.video.url
        video_title = swgrsmedia.video_title
    else:
        video = ""
        video_title = ""
    return {'post': swgrsmedia, 'post_time': dt, 'video': video, 'video_title': video_title}


@register.inclusion_tag('hobro/embed_swgrssong.html')
def embed_swgrssong(swgrssong):
    swgrssong = swgrssong.first()
    embed_sc = make_soundcloud_embed(swgrssong)
    return {'song': swgrssong, 'embed_code_sc': embed_sc}
