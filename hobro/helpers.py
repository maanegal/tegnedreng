from .models import *
from datetime import datetime


def str_to_int(s):
    try:
        i = int(s)
    except ValueError:
        i = None
    return i


def class_from_str(name):
    if name == 'post':
        return Post
    elif name in ('postphoto', 'post-photo'):
        return PostPhoto
    elif name in ('postvideo', 'post-video'):
        return PostVideo
    elif name in ('profileevent', 'profile-event'):
        return ProfileEvent
    elif name == 'character':
        return Character
    elif name in ('itemembed', 'item-embed'):
        return ItemEmbed
    elif name == 'story':
        return Story
    elif name == 'section':
        return Section
    elif name == 'album':
        return Album
    elif name == 'song':
        return Song
    elif name in ('musicvideo', 'music-video'):
        return MusicVideo
    elif name == 'hashtag':
        return Hashtag
    elif name == 'swgrs_song':
        return SwgrsSong
    elif name == 'swgrs_post':
        return SwgrsPost
    elif name == 'swgrs_media':
        return SwgrsMedia
    elif name == 'comment':
        return Comment
    elif name == 'motif':
        return Motif
    else:
        print('unknown class:', name)
        return None


def object_from_alias(alias):
    """From an alias or timestamp, get the associated object"""
    o = Section.objects.filter(time_stamp=str_to_int(alias)).first()
    if o:
        return o
    o = Story.objects.filter(time_stamp=str_to_int(alias)).first()
    if o:
        return o
    o = Character.objects.filter(alias=str(alias)).first()
    if o:
        return o
    o = Post.objects.filter(time_stamp=str_to_int(alias)).first()
    if o:
        return o
    o = PostPhoto.objects.filter(time_stamp=str_to_int(alias)).first()
    if o:
        return o
    o = PostVideo.objects.filter(time_stamp=str_to_int(alias)).first()
    if o:
        return o
    o = ProfileEvent.objects.filter(time_stamp=str_to_int(alias)).first()
    if o:
        return o
    o = ItemEmbed.objects.filter(time_stamp=str_to_int(alias)).first()
    if o:
        return o
    o = Album.objects.filter(alias=str(alias)).first()
    if o:
        return o
    o = Song.objects.filter(alias=str(alias)).first()
    if o:
        return o
    o = MusicVideo.objects.filter(alias=str(alias)).first()
    if o:
        return o
    o = Hashtag.objects.filter(slug=str(alias)).first()
    if o:
        return o
    o = SwgrsPost.objects.filter(time_stamp=str_to_int(alias)).first()
    if o:
        return o
    o = SwgrsMedia.objects.filter(time_stamp=str_to_int(alias)).first()
    if o:
        return o
    o = SwgrsSong.objects.filter(alias=str(alias)).first()
    if o:
        return o
    o = Comment.objects.filter(alias=str(alias)).first()
    if o:
        return o
    o = Motif.objects.filter(alias=str(alias)).first()
    if o:
        return o
    if not o:
        print('failed getting', alias)


def get_current_info(ts):
    """Get the page name and photo for a certain point in time. Takes datetime or int (epoch timestamp)"""
    if isinstance(ts, datetime):
        ts = int(ts.timestamp())
    if not isinstance(ts, int):
        return None
    data = ProfileEvent.objects.filter(expires__gt=ts, time_stamp__lt=ts).first()
    hit = {'name': data.page_name, 'photo': data.photo}
    return hit


def get_current_section(ts):
    """Get the current Section object for a certain point in time. Takes datetime or int (epoch timestamp)"""
    if isinstance(ts, datetime):
        ts = int(datetime.strftime(ts))
    if not isinstance(ts, int):
        return None
    data = Section.objects.filter(expires__gt=ts, time_stamp__lt=ts).first()
    return data


def set_expirations():
    """For Section and ProfileEvent objects, calculate the end point"""
    sec = Section.objects.all()
    ev = ProfileEvent.objects.all()
    for t in [sec, ev]:
        timestamps = []
        for s in t:
            if s.expires:
                continue
            timestamps.append(s.time_stamp)
        timestamps.sort()
        results = {}
        for index, stamp in enumerate(timestamps):
            if index < len(timestamps):
                next_index = index + 1
                try:
                    exp = timestamps[next_index] - 1
                except:
                    exp = int(datetime.now().timestamp())
            else:  # for the last item, just get the current time as expiration, to be way on the safe side
                exp = int(datetime.now().timestamp())
            results[stamp] = exp
        for k, v in results.items():
            o = t.filter(time_stamp=k).first()
            o.expires = v
            o.save(update_fields=['expires'])


def make_relations(data):
    """Put relationships into db once the objects have been saved.
    Takes dict with object alias as key, and list of tuples as values. Tuples are field and target object alias"""
    one_to_ones = ['album', 'song', 'on_story', 'on_profileevent', 'on_post', 'on_postphoto', 'on_postvideo',
                   'on_swgrspost', 'on_swgrsmedia', 'on_character', 'on_song', 'on_album', 'on_musicvideo',
                   'on_swgrssong', 'on_itemembed']
    for k, v in data.items():
        try:
            parent = object_from_alias(k)
            for r in v:
                rel = r[0]
                target = object_from_alias(r[1])
                if rel in one_to_ones:
                    setattr(parent, rel, target)
                else:
                    try:
                        parent.__getattribute__(rel).add(target)
                    except Exception as e:
                        print(e, rel, parent, target, r, k)
            parent.save()
        except:
            print('Error making relation. Relation:', rel, 'Parent:', parent, 'alias:', k, 'Target:', target, r, v)


def the_big_retriever(number=None):
    """Right now, just the first one"""
    content = {}
    id_list = []
    objects = []
    if number:
        number -= 1
        sections = [Section.objects.all()[number]]
    else:
        sections = Section.objects.all()
    for section in sections:
        stamp_start = section.time_stamp
        stamp_end = section.expires
        id_list.append(stamp_start)
        content[stamp_start] = section
        objects.extend(list(Post.objects.filter(time_stamp__lt=stamp_end, time_stamp__gt=stamp_start)))
        objects.extend(list(PostPhoto.objects.filter(time_stamp__lt=stamp_end, time_stamp__gt=stamp_start)))
        objects.extend(list(PostVideo.objects.filter(time_stamp__lte=stamp_end, time_stamp__gte=stamp_start)))
        objects.extend(list(Section.objects.filter(time_stamp__lt=stamp_end, time_stamp__gt=stamp_start)))
        objects.extend(list(Story.objects.filter(time_stamp__lte=stamp_end, time_stamp__gte=stamp_start)))
        objects.extend(list(ProfileEvent.objects.filter(time_stamp__lt=stamp_end, time_stamp__gt=stamp_start)))
        objects.extend(list(SwgrsPost.objects.filter(time_stamp__lt=stamp_end, time_stamp__gt=stamp_start)))
        objects.extend(list(SwgrsMedia.objects.filter(time_stamp__lt=stamp_end, time_stamp__gt=stamp_start)))
        objects.extend(list(ItemEmbed.objects.filter(time_stamp__lt=stamp_end, time_stamp__gt=stamp_start)))
    for o in objects:
        content[o.time_stamp] = o
        id_list.append(o.time_stamp)

    id_list.sort()
    output = []

    for id in id_list:
        o = content.get(id)
        output.append(o)

    return output


def get_layout(lt=""):
    # basic placement:
    if 'left' in lt:
        outer = ""
        inner = "left is-6-desktop is-8-tablet is-offset-1"
    elif 'right' in lt:
        outer = ""
        inner = "right is-6-desktop is-8-tablet is-offset-5-desktop is-offset-3-tablet"
    elif 'notecard' in lt:  # for story elements
        outer = "is-centered"
        inner = "is-6-desktop is-8-tablet notecard"
    else:
        outer = "is-centered"
        inner = "is-6-desktop is-8-tablet"
    # background type:
    if 'color-b' in lt:
        outer += " background-party"
    elif 'color-c' in lt:
        outer += " background-release"
    elif 'color-a' in lt:
        outer += " background-main"
    elif 'bg-swgrs' in lt:
        outer += " background-swgrs"
    elif 'bg-dark' in lt:
        outer += " background-dark"
    elif 'paper' in lt:
        outer += " paper"
    elif 'faded-paper' in lt:
        outer += " faded-paper"
    else:
        outer += " background-main"
    # dimensional effect:
    if 'raised' in lt:
        outer += " is-raised"
    elif 'sunk' in lt:
        outer += " is-sunk"
    elif 'stacked' in lt:
        outer += " is-stacked"
    # section size:
    if 'big' in lt:
        outer += " is-medium"
    elif 'bigger' in lt:
        outer += " is-large"
    if 'justified' in lt:
        inner += " justified"
    return outer, inner


def make_bandcamp_embed(album=None, song=None):
    if album and song:
        a = '<iframe style="border: 0; width: 100%; height: 42px;" class="lazy" data-src="https://bandcamp.com/EmbeddedPlayer/album='
        b = '/size=small/bgcol=ffffff/linkcol=0687f5/track='
        c = '/transparent=true/" seamless><a href="'
        d = '">'
        f = '</a></iframe>'
        e = a + album.bc_embed_code + b + song.bc_embed_code + c + song.link_bc + d + song.title + f
    elif song:
        a = '<iframe style="border: 0; width: 100%; height: 42px;" class="lazy" data-src="https://bandcamp.com/EmbeddedPlayer/track='
        b = '/size=small/bgcol=ffffff/linkcol=0687f5/transparent=true/" seamless><a href="'
        c = '">'
        d = '</a></iframe>'
        e = a + song.bc_embed_code + b + song.link_bc + c + song.title + d
    elif album:
        a = '<iframe id="' + album.bc_embed_code + '"style="border: 0; width: 100%; height: 500px;" class="lazy" data-src="https://bandcamp.com/EmbeddedPlayer/album='
        b = '/size=large/bgcol=ffffff/linkcol=333333/artwork=small/transparent=true/" seamless><a href="'
        c = '">'
        d = '</a></iframe>'
        e = a + album.bc_embed_code + b + album.link_bc + c + album.title + d
    else:
        e = None
    return e


def make_spotify_embed(album=None, song=None):
    e = None
    if album:
        a = '<iframe class="lazy" data-src="https://open.spotify.com/embed/album/'
        b = '" width="100%" height="500" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>'
        if album.sp_embed_code:
            e = a + album.sp_embed_code + b
    elif song:
        a = '<iframe class="lazy" data-src="https://open.spotify.com/embed/track/'
        b = '" width="100%" height="80" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>'
        if song.sp_embed_code:
            e = a + song.sp_embed_code + b
    return e


def make_youtube_embed(obj):
    a = '<iframe class="lazy" width="560" height="315" class="lazy" data-src="https://www.youtube.com/embed/'
    b = '" frameborder="0" allow="accelerometer; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'
    c = obj.link_yt.split('=')[-1]
    e = a + c + b
    return e


def make_soundcloud_embed(obj):
    a = '<iframe class="lazy" width="100%" height="166" scrolling="no" frameborder="no" allow="autoplay" class="lazy" data-src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/'
    b = '&color=%231a1a1a&auto_play=false&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true"></iframe>'
    e = None
    if obj.sc_embed_code:
        e = a + obj.sc_embed_code + b

    return e
