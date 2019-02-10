
def loader(files=[]):
    items = []
    objects = []
    for file in files:
        i = mark_it_down(file)
        items.append(i)
    for item in items:
        objects.append(process_tree(item))

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
            cur_item[elem].append(s)
        elif line.startswith(body_head):  # body section of item has been opened
            load_body = True

    return output


def process_tree(item={}):
    element = item['id']
    obj = None
    if element == 'post':
        obj = None
    elif element == 'post-photo':
        obj = None
    elif element == 'post-video':
        obj = None
    elif element == 'profile-event':
        obj = None
    elif element == 'item-embed':
        # set alias (timestamp)
        # expect embed prop with the alias of another element
        obj = None
    elif element == 'section':
        # set alias (timestamp)
        # expect a text element with two values -- chapter number and title. Render to HTML as h2, split up somehow
        obj = None
    elif element == 'story':
        # set alias (timestamp)
        # expect either text or body element
        # parse them from markdown to HTML. Locate URLs and hashtags and mentions.
        # Make URLs live. Make hashtags relate to a master object. Set mentions bold
        obj = None
    elif element == 'character':
        obj = None
    elif element == 'album':
        obj = None
    elif element == 'song':
        obj = None
    elif element == 'music-video':
        obj = None
    return obj
