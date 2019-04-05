from datetime import datetime
from ..models import *
from hobro.helpers import get_current_info, make_bandcamp_embed, make_spotify_embed, make_youtube_embed, \
    make_soundcloud_embed, get_layout
from django import template
register = template.Library()


@register.inclusion_tag('hobro/post.html')
def show_post(post, anim_pref):
    info = get_current_info(post.time_stamp)
    dt = datetime.fromtimestamp(post.time_stamp)
    outer, inner = get_layout(post.layout)
    return {'post': post, 'name': info.get('name', ''), 'profilepic': info.get('photo', ''), 'post_time': dt,
            'layout_outer': outer, 'layout_inner': inner, "anim_pref": anim_pref}


@register.inclusion_tag('hobro/postphoto.html')
def show_postphoto(postphoto, anim_pref):
    info = get_current_info(postphoto.time_stamp)
    dt = datetime.fromtimestamp(postphoto.time_stamp)
    outer, inner = get_layout(postphoto.layout)
    return {'post': postphoto, 'name': info.get('name', ''), 'profilepic': info.get('photo', ''), 'post_time': dt,
            'layout_outer': outer, 'layout_inner': inner, "anim_pref": anim_pref}


@register.inclusion_tag('hobro/postvideo.html')
def show_postvideo(postvideo, anim_pref):
    info = get_current_info(postvideo.time_stamp)
    dt = datetime.fromtimestamp(postvideo.time_stamp)
    outer, inner = get_layout(postvideo.layout)
    return {'post': postvideo, 'name': info.get('name', ''), 'profilepic': info.get('photo', ''), 'post_time': dt,
            'layout_outer': outer, 'layout_inner': inner, "anim_pref": anim_pref}


@register.inclusion_tag('hobro/post_card.html')
def show_post_card(post, swgrs=False):
    info = get_current_info(post.time_stamp)
    dt = datetime.fromtimestamp(post.time_stamp)
    return {'post': post, 'name': info.get('name', ''), 'profilepic': info.get('photo', ''), 'post_time': dt, 'is_swgrs': swgrs}


@register.inclusion_tag('hobro/section.html')
def show_section(section):
    return {'section': section}


@register.inclusion_tag('hobro/story.html')
def show_story(story, anim_pref):
    if story.layout:
        layout = story.layout
    else:
        layout = "sunk paper"
    outer, inner = get_layout(layout)
    return {'story': story, 'layout_outer': outer, 'layout_inner': inner, 'anim_pref': anim_pref}


@register.inclusion_tag('hobro/profileevent.html')
def show_profileevent(profileevent, anim_pref):
    dt = datetime.fromtimestamp(profileevent.time_stamp)
    #if profileevent.layout:
     #   layout = profileevent.layout
    #else:
    layout = "color-c"
    outer, inner = get_layout(layout)
    return {'profileevent': profileevent, 'post_time': dt, 'layout_outer': outer, 'layout_inner': inner, 'anim_pref': anim_pref}


@register.inclusion_tag('hobro/swgrspost.html')
def show_swgrspost(swgrspost, anim_pref):
    dt = datetime.fromtimestamp(swgrspost.time_stamp)
    if swgrspost.layout:
        layout = swgrspost.layout
    else:
        layout = "bg-swgrs"
    outer, inner = get_layout(layout)
    yt = ""
    try:
        if swgrspost.link_yt:
            yt = make_youtube_embed(swgrspost)
    except:
        yt = ""
    return {'swgrspost': swgrspost, 'post_time': dt, 'yt_embed': yt, 'layout_outer': outer, 'layout_inner': inner, "anim_pref": anim_pref}


@register.inclusion_tag('hobro/swgrsmedia.html')
def show_swgrsmedia(swgrsmedia, anim_pref):
    dt = datetime.fromtimestamp(swgrsmedia.time_stamp)
    if swgrsmedia.layout:
        layout = swgrsmedia.layout
    else:
        layout = "bg-swgrs"
    outer, inner = get_layout(layout)
    if swgrsmedia.video:
        video = swgrsmedia.video.url
        video_title = swgrsmedia.video_title
    else:
        video = ""
        video_title = ""
    return {'post': swgrsmedia, 'post_time': dt, 'video': video, 'video_title': video_title, 'layout_outer': outer,
            'layout_inner': inner, "anim_pref": anim_pref}


@register.inclusion_tag('hobro/itemembed.html')
def show_itemembed(itemembed, anim_pref):
    dt = datetime.fromtimestamp(itemembed.time_stamp)
    kind = itemembed.what_kind()
    outer, inner = get_layout("")
    return {'itemembed': itemembed, 'post_time': dt, 'kind': kind, 'layout_outer': outer, "anim_pref": anim_pref}


@register.inclusion_tag('hobro/embed_song.html')
def embed_song(song, layout, anim_pref):
    s = song.first()
    a = None
    if s.album:
        a = s.album
    embed_bc = make_bandcamp_embed(album=a, song=s)
    embed_sp = make_spotify_embed(album=None, song=s)
    outer, inner = get_layout(layout)
    return {'song': s, 'embed_code_bc': embed_bc, 'embed_code_sp': embed_sp, 'layout_outer': outer,
            'layout_inner': inner, "anim_pref": anim_pref}


@register.inclusion_tag('hobro/embed_album.html')
def embed_album(album, anim_pref, layout=""):
    al = album.first()
    embed_bc = make_bandcamp_embed(album=al, song=None)
    embed_sp = make_spotify_embed(album=al, song=None)
    outer, inner = get_layout(layout)
    return {'album': al, 'embed_code_bc': embed_bc, 'embed_code_sp': embed_sp, 'layout_outer': outer,
            'layout_inner': inner, "anim_pref": anim_pref}


@register.inclusion_tag('hobro/embed_musicvideo.html')
def embed_musicvideo(musicvideo, anim_pref):
    embed = make_youtube_embed(musicvideo.first())
    return {'musicvideo': musicvideo.first(), 'embed_code': embed, "anim_pref": anim_pref}


@register.inclusion_tag('hobro/embed_character.html')
def embed_character(character):
    return {'character': character.first()}


@register.inclusion_tag('hobro/embed_swgrssong.html')
def embed_swgrssong(swgrssong, anim_pref):
    swgrssong = swgrssong.first()
    embed_sc = make_soundcloud_embed(swgrssong)
    return {'song': swgrssong, 'embed_code_sc': embed_sc, "anim_pref": anim_pref}


@register.inclusion_tag('hobro/comment.html')
def show_comment(comment, pref, motifs_seen, anim_pref):
    return {'comment': comment, 'pref': pref, 'motifs_seen': motifs_seen, "anim_pref": anim_pref}
