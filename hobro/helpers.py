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
    else:
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
    one_to_ones = ['album', 'song']
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
            print(rel, parent, target, r, k, v)


def the_big_retriever(index=None):
    """Right now, just the first one"""
    content = {}
    id_list = []
    objects = []
    if index:
        sections = [Section.objects.all()[index]]
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


def make_bandcamp_embed(album=None, song=None):
    if album and song:
        print(album, song)
        a = '<iframe style="border: 0; width: 100%; height: 42px;"src="https://bandcamp.com/EmbeddedPlayer/album='
        b = '/size=small/bgcol=ffffff/linkcol=0687f5/track='
        c = '/transparent=true/" seamless><a href="'
        d = '">'
        f = '</a></iframe>'
        e = a + album.bc_embed_code + b + song.bc_embed_code + c + song.link_bc + d + song.title + f
    elif song:
        a = '<iframe style="border: 0; width: 100%; height: 42px;" src="https://bandcamp.com/EmbeddedPlayer/track='
        b = '/size=small/bgcol=ffffff/linkcol=0687f5/transparent=true/" seamless><a href="'
        c = '">'
        d = '</a></iframe>'
        e = a + song.bc_embed_code + b + song.link_bc + c + song.title + d
    elif album:
        a = '<iframe style="border: 0; width: 700px; height: 500px;" src="https://bandcamp.com/EmbeddedPlayer/album='
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
        a = '<iframe src="https://open.spotify.com/embed/album/'
        b = '" width="700" height="500" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>'
        if album.sp_embed_code:
            e = a + album.sp_embed_code + b
    elif song:
        a = '<iframe src="https://open.spotify.com/embed/track/'
        b = '" width="700" height="80" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>'
        if song.sp_embed_code:
            e = a + song.sp_embed_code + b
    return e


def make_youtube_embed(obj):
    a = '<iframe width="560" height="315" src="https://www.youtube.com/embed/'
    b = '" frameborder="0" allow="accelerometer; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'
    c = obj.link_yt.split('=')[-1]
    e = a + c + b
    return e
