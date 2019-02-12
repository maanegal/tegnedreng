from .models import *
from pathlib import Path
import os
import re
from datetime import datetime
from markdown import markdown
from .helpers import set_expirations, make_relations, str_to_int


# This is the master list of hashtags. Commit it to database after ingest. Key is hashtag, value is a list of aliases
hashtags = {}
WEB_URL_REGEX = r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"""

temp_path = "E:/Dropbox/Månegal/Tegnedreng Records/content"


def loader(files=[]):
    items = []
    objects = 0
    relations = {}
    for file in files:
        print("working on", file)
        with open(file, 'r', encoding='utf8') as filehandle:
            content = filehandle.read()
        i = mark_it_down(content)
        for u in i:
            items.append(u)
    print('markdown done.', len(items), 'found')
    for item in items:
        obj, rel = process_tree(item)
        if obj:
            obj.save()
            try:
                val = obj.alias
            except:
                val = obj.time_stamp
            relations[val] = rel
            objects += 1
        else:
            pass
            # print(item)
    print('interpretation done.', objects, 'processed')
    set_expirations()
    print('expirations done')
    make_relations(relations)
    print('relations done\nAll done!')


def folder_loader(path):
    folder = Path(path)
    filenames = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f)) and f.endswith('.md')]
    files = []
    for file in filenames:
        files.append(os.path.join(folder, file))
    objects = loader(files)
    return objects


def mark_it_down(data):
    content = data.splitlines()
    item = "## "
    element = "* "
    sub = "  "
    body_head = "### body"
    br = "\n"

    output = []  # list of each item parsed from data

    cur_item = {}  # active item, demarcated by 'item' lines. Appended to output and emptied when new item starts
    elem = ""
    body = ""  # store free text
    load_body = False

    for line in content:
        if load_body:  # if body section was called in item
            if not line.startswith(item):
                body += line + br
                continue  # don't go through other checks; this is read as plain text
            else:
                load_body = False  # This is a new item head, meaning body section is over. Next line goes right ahead

        if line.startswith(item):
            if cur_item:  # file previous item and start a new one
                if body:  # if item has body section, attach it and clear var
                    cur_item['body'] = body
                    body = ""
                output.append(cur_item)
                cur_item = {}
            cur_item['id'] = line[len(item):]  # get line without the prefix
        elif line.startswith(element):
            elem = line[len(element):]  # get line without the prefix and set as current element
            cur_item[elem] = []  # store element in current item, with empty list as value
        elif line.startswith(sub):  # line is indented
            if not elem:  # store value, even if elem is somehow not set
                elem = "unknown"
            s = line.replace('*', '').strip()  # get line without the prefix
            if s.startswith('|'):  # remove the temporary '|' prefix
                s = s[2:]
            try:
                cur_item[elem].append(s)
            except Exception as e:
                print(line, cur_item)
                raise
        elif line.startswith(body_head):  # body section of item has been opened
            load_body = True
    if body:  # write final item
        cur_item['body'] = body
    output.append(cur_item)
    return output


def html_element(tag='div', id="", classes=[], custom={}):
    """make a valid HTML element, with open and close tags and optional classes and id.
    Custom should be a dict of property as key, value as value"""
    close_tag = '</'+tag+'>'
    open_tag = '<'+tag
    if id:
        open_tag += ' id="'+id+'"'
    if classes:
        open_tag += ' class="'.join(classes)
        open_tag += '"'
    if custom:
        for k, v in custom.items():
            open_tag += ' ' + k + '="' + v + '"'
    open_tag += '>'
    return open_tag, close_tag


def render_html(data):
    html = ""
    return html


def make_links(text):
    """Find URLs in string and replace with html-links"""
    urls = re.findall(WEB_URL_REGEX, text)
    for url in urls:
        if not url.startswith('http'): # don't interpret partial links as relative, thank you very much
            url = 'http://' + url
        html_o, html_c = html_element('a', custom={'href': url})
        tag = html_o + url + html_c
        t2 = text.replace(url, tag)
        text = t2
    return text


def make_hashtags(text, alias):
    """Take string of text. Split into words. If a word starts with #, it's a hashtag.
    Add alias to that hashtag's entry in the master list.
    Transform the word to an HTML link. Initially, just a '#' target.
    """
    words = text.split(' ')
    new_words = []
    ht = []
    for word in words:
        if '#' in word and not word.endswith('#'):
            ht.append(word)
            # make word a link
            html_o, html_c = html_element('a', custom={'href': '#'})
            word = html_o + word + html_c
        new_words.append(word)
    for tag in ht:
        if hashtags.get(tag):
            hashtags[tag].append(alias)
        else:
            hashtags[tag] = [alias]
    new_text = " ".join(new_words)
    return new_text


def make_mentions(text):
    words = text.split(' ')
    new_words = []
    for word in words:
        if '@' in word and not word.endswith('@'):
            html_o, html_c = html_element('strong')
            word = html_o + word + html_c
        new_words.append(word)
    new_text = " ".join(new_words)
    return new_text


def parse_relation(field, r):
    relations = []
    if r:
        for a in r:
            relations.append((field, a))
    return relations


def process_tree(item={}):
    relations = []
    element = item['element'][0]
    alias = item['id']
    text = None
    if item.get('body', None):
        text = item.get('body', None)
    elif item.get('text', None):
        text = item.get('text', None)[0]
    obj = None
    if element == 'post':
        if not text:
            return None
        html = markdown(text)
        html = make_links(html)
        html = make_hashtags(html, alias)
        html = make_mentions(html)
        link_fb = item.get('link_fb', '')
        link_tw = item.get('link_tw', '')
        relations.extend(parse_relation('appears', item.get('appears', None)))
        obj = Post(text=html, time_stamp=int(alias), link_fb=link_fb, link_tw=link_tw)
    elif element == 'post-photo':
        if not text:
            return None
        html = markdown(text)
        html = make_links(html)
        html = make_hashtags(html, alias)
        html = make_mentions(html)
        link_fb = item.get('link_fb', '')
        link_tw = item.get('link_tw', '')
        link_ig = item.get('link_ig', '')
        relations.extend(parse_relation('appears', item.get('appears', None)))
        obj = PostPhoto(text=html, time_stamp=int(alias), photo=item.get('photo'),
                        link_fb=link_fb, link_tw=link_tw, link_ig=link_ig)
    elif element == 'post-video':
        if not text:
            return None
        html = markdown(text)
        html = make_links(html)
        html = make_hashtags(html, alias)
        html = make_mentions(html)
        link_fb = item.get('link_fb', '')
        link_tw = item.get('link_tw', '')
        link_ig = item.get('link_ig', '')
        title = item.get('title', '')
        if title:
            title = title[0]
        else:
            title = None
        relations.extend(parse_relation('appears', item.get('appears', None)))
        obj = PostVideo(text=html, time_stamp=int(alias), title=title, video=item.get('video')[0],
                            photo=item.get('photo', '')[0], link_fb=link_fb, link_tw=link_tw, link_ig=link_ig)
    elif element == 'profile-event':
        if not text:
            text = ''
        html = markdown(text)
        html = make_links(html)
        link_fb = item.get('link_fb', '')
        al = int(alias)
        obj = ProfileEvent(time_stamp=al, photo=item.get('photo')[0], text=html, page_name=item.get('name')[0],
                           link_fb=link_fb)
    elif element == 'item-embed':
        # set alias (timestamp)
        # expect embed prop with the alias of another element
        obj = ItemEmbed(time_stamp=int(alias))
    elif element == 'section':
        # set alias (timestamp)
        # expect a text element with two values -- chapter number and title. Render to HTML as h2, split up somehow
        if not text:
            return None
        html_o, html_c = html_element('h2')
        html = html_o + text + html_c
        obj = Section(text=html, time_stamp=int(alias))
    elif element == 'story':
        # set alias (timestamp)
        # expect either text or body element
        # parse them from markdown to HTML. Locate URLs and hashtags and mentions.
        # Make URLs live. Make hashtags relate to a master object. Set mentions bold
        if not text:
            return None
        html = markdown(text)
        html = make_links(html)
        html = make_hashtags(html, alias)
        html = make_mentions(html)
        obj = Story(text=html, time_stamp=int(alias))
    elif element == 'character':
        if not text:
            text = ''
        html = make_links(text)
        html = make_hashtags(html, alias)
        html = make_mentions(html)
        obj = Character(alias=alias, name=item.get('name')[0], photo=item.get('photo')[0], text=html)
    elif element == 'music-album':
        if not text:
            text = ''
        html = make_links(text)
        html = make_hashtags(html, alias)
        html = make_mentions(html)
        rel = item.get('release_date')[0]
        dt = datetime.fromtimestamp(int(rel))
        obj = Album(alias=alias, title=item.get('title')[0], link_bc=item.get('url')[0], text=html, release_date=dt)
    elif element == 'music-song':
        if not text:
            text = ''
        html = make_links(text)
        html = make_hashtags(html, alias)
        html = make_mentions(html)
        link_bc = item.get('url')[0]
        track = item.get('track_number', None)
        if track:
            track = str_to_int(track[0])
        else:
            track = None
        relations.extend(parse_relation('appears', item.get('featuring', None)))
        relations.extend(parse_relation('producer', item.get('producer', None)))
        relations.extend(parse_relation('album', item.get('album', None)))
        obj = Song(alias=alias, title=item.get('title')[0], link_bc=link_bc,
                   text=html, track_number=track)
    elif element == 'music-video':
        if not text:
            text = ''
        html = make_links(text)
        html = make_hashtags(html, alias)
        html = make_mentions(html)
        yt = item.get('link-yt')[0]
        relations.extend(parse_relation('appears', item.get('appears', None)))
        relations.extend(parse_relation('song', item.get('video-for', None)))
        obj = MusicVideo(alias=alias, title=item.get('title')[0], embed_url=yt, link_yt=yt, text=html)
    if not obj:
        print(element, alias)
    return obj, relations






# Store relationships in var while doing initial create. Save objects to db
# Second round: Load relationship list and set them. Calculate expiration for profile info objects
