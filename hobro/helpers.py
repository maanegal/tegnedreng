from .models import *
from datetime import datetime


def str_to_int(s):
    try:
        i = int(s)
    except ValueError:
        i = None
    return i


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


def get_current_info(ts):
    """Get the page name and photo for a certain point in time. Takes datetime or int (epoch timestamp)"""
    if isinstance(ts, datetime):
        ts = int(ts.timestamp())
    if not isinstance(ts, int):
        return None
    data = ProfileEvent.objects.filter(expires__lte=ts, time_stamp__gte=ts).first()
    hit = {'name': data.page_name, 'photo': data.photo}
    return hit


def get_current_section(ts):
    """Get the current Section object for a certain point in time. Takes datetime or int (epoch timestamp)"""
    if isinstance(ts, datetime):
        ts = int(datetime.strftime(ts))
    if not isinstance(ts, int):
        return None
    data = Section.objects.filter(expires__lte=ts, time_stamp__gte=ts).first()
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
        parent = object_from_alias(k)
        for r in v:
            rel = r[0]
            target = object_from_alias(r[1])
            if rel in one_to_ones:
                setattr(parent, rel, target)
            else:
                try:
                    parent.__getattribute__(rel).add(target)
                except:
                    print(rel, parent, target, r, k)
        parent.save()
