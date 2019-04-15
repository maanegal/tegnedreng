from django.db import models
from django.utils.text import slugify
from datetime import datetime

# BASIC STORY ELEMENTS
class Section(models.Model):
    """Sections in the story. Plain text, renders to HTML headings H2. Timestamps are purely for sorting here"""
    time_stamp = models.IntegerField()
    slug = models.SlugField(unique=True)
    number = models.CharField(max_length=2)
    text = models.CharField(max_length=200)
    expires = models.IntegerField(null=True)  # one less than value of next object

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.time_stamp))
        super(Section, self).save(*args, **kwargs)

    def get_type(self):
        class_name = "section"
        return class_name


class Story(models.Model):
    """Blocks of text describing the story. Formatted as HTML. Timestamps are purely for sorting here"""
    time_stamp = models.IntegerField()
    slug = models.SlugField(unique=True)
    text = models.TextField()
    layout = models.CharField(max_length=30, default='sunk paper justified')  # how the post should appear. Select from html presets

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.time_stamp))
        super(Story, self).save(*args, **kwargs)

    def get_type(self):
        class_name = "story"
        return class_name


class Character(models.Model):
    """Information on a character in the story"""
    alias = models.CharField(max_length=30)
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=100)
    photo = models.ImageField(default="default.jpg")  # filename of photo, stored in folder
    text = models.TextField()  # in case a description is needed

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Character, self).save(*args, **kwargs)

    def get_type(self):
        class_name = "character"
        return class_name


# POST ELEMENTS
class Post(models.Model):
    """Basic post items. Includes Link items"""
    time_stamp = models.IntegerField()
    slug = models.SlugField(unique=True)
    text = models.TextField()
    page_name = models.CharField(max_length=60)  # link to profile-event via function
    layout = models.CharField(max_length=30, default='')  # how the post should appear. Select from html presets
    appears = models.ManyToManyField(Character) # Set characters that appear in this post
    link_fb = models.CharField(max_length=100, null=True)  # facebook post id
    link_tw = models.CharField(max_length=100, null=True)  # twitter post id

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.time_stamp))
        super(Post, self).save(*args, **kwargs)

    def get_type(self):
        class_name = "post"
        return class_name


class PostPhoto(models.Model):
    """Photo post items. References a locally stored image. Includes Link items"""
    time_stamp = models.IntegerField()
    slug = models.SlugField(unique=True)
    text = models.TextField()  # photo description
    photo = models.ImageField(default="default.jpg")  # filename of photo, stored in folder
    page_name = models.CharField(max_length=60)  # link to profile-event via function
    layout = models.CharField(max_length=30, default='')  # how the post should appear. Select from html presets
    appears = models.ManyToManyField(Character)  # Set characters that appear in this post
    link_fb = models.CharField(max_length=100, null=True)  # facebook post id
    link_ig = models.CharField(max_length=100, null=True)  # instagram post id
    link_tw = models.CharField(max_length=100, null=True)  # twitter post id

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.time_stamp))
        super(PostPhoto, self).save(*args, **kwargs)

    def get_type(self):
        class_name = "postphoto"
        return class_name


class PostVideo(models.Model):
    """Video post items. References a locally stored video file. Includes Link items"""
    time_stamp = models.IntegerField()
    slug = models.SlugField(unique=True)
    text = models.TextField()  # video description
    video = models.FileField()  # filename of video, stored in folder
    title = models.CharField(max_length=160, null=True)  # title of video
    photo = models.ImageField(default="default.jpg")  # filename of photo, stored in folder
    page_name = models.CharField(max_length=60)  # link to profile-event via function
    layout = models.CharField(max_length=30, default='')  # how the post should appear. Select from html presets
    appears = models.ManyToManyField(Character)  # Set characters that appear in this post
    link_fb = models.CharField(max_length=100, null=True)  # facebook post id
    link_ig = models.CharField(max_length=100, null=True)  # instagram post id
    link_tw = models.CharField(max_length=100, null=True)  # twitter post id

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.time_stamp))
        super(PostVideo, self).save(*args, **kwargs)

    def get_type(self):
        class_name = "postvideo"
        return class_name


class ProfileEvent(models.Model):
    """Posts indicating changes in the online presence, such as new profile picture or page name"""
    time_stamp = models.IntegerField()
    slug = models.SlugField(unique=True)
    expires = models.IntegerField(null=True)  # one less than value of next object
    page_name = models.CharField(max_length=60)  # link to profile-event via function
    photo = models.ImageField(default="default.jpg")  # filename of photo, stored in folder
    photo_thumb = models.ImageField(default="default.jpg")  # filename of photo, stored in folder
    text = models.TextField()  # free text field, in case it is needed
    link_fb = models.CharField(max_length=100, null=True)  # facebook post id
    link_tw = models.CharField(max_length=100, null=True)  # twitter post id

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.time_stamp))
        super(ProfileEvent, self).save(*args, **kwargs)

    def get_type(self):
        class_name = "profileevent"
        return class_name


class Album(models.Model):
    """An album, containing songs"""
    alias = models.CharField(max_length=30)
    slug = models.SlugField(unique=True)
    photo = models.ImageField(default="default.jpg")  # filename of photo, stored in folder
    title = models.CharField(max_length=100)
    text = models.TextField()  # description
    name = models.CharField(max_length=100, default="Tegnedreng Records")
    release_date = models.DateField()
    bc_embed_code = models.CharField(max_length=100)  # code used for bandcamp embeds
    sp_embed_code = models.CharField(max_length=100, null=True)  # code used for spotify embeds
    link_yt = models.CharField(max_length=100, null=True)  # youtube
    link_bc = models.CharField(max_length=100, null=True)  # bandcamp
    link_sp = models.CharField(max_length=100, null=True)  # spotify
    link_sc = models.CharField(max_length=100, null=True)  # soundcloud
    link_it = models.CharField(max_length=100, null=True)  # itunes

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Album, self).save(*args, **kwargs)

    def get_type(self):
        class_name = "album"
        return class_name


class Song(models.Model):
    """A song. Most belong to an album"""
    alias = models.CharField(max_length=30)
    slug = models.SlugField(unique=True)
    photo = models.ImageField(default="default.jpg")  # filename of photo, stored in folder
    title = models.CharField(max_length=100)
    track_number = models.IntegerField(null=True)
    text = models.TextField()  # description
    lyrics = models.TextField()
    bc_embed_code = models.CharField(max_length=100)  # code used for bandcamp embeds
    sp_embed_code = models.CharField(max_length=100, null=True)  # code used for spotify embeds
    link_yt = models.CharField(max_length=100, null=True)  # youtube
    link_bc = models.CharField(max_length=100, null=True)  # bandcamp
    link_sp = models.CharField(max_length=100, null=True)  # spotify
    link_sc = models.CharField(max_length=100, null=True)  # soundcloud
    link_it = models.CharField(max_length=100, null=True)  # itunes
    appears = models.ManyToManyField(Character, related_name='appears_on_song')
    producer = models.ManyToManyField(Character, related_name='producer')
    album = models.ForeignKey(Album, null=True, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Song, self).save(*args, **kwargs)

    def get_type(self):
        class_name = "song"
        return class_name


class MusicVideo(models.Model):
    """An album, containing songs"""
    alias = models.CharField(max_length=30)
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=100)
    text = models.TextField()  # description
    release_date = models.DateField(null=True)
    embed_url = models.CharField(max_length=100)  # url used embedding item player
    link_yt = models.CharField(max_length=100, null=True)  # youtube
    appears = models.ManyToManyField(Character, related_name='appears_in_video')
    song = models.OneToOneField(Song, null=True, on_delete=models.CASCADE)  # The song featured in the music video

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(MusicVideo, self).save(*args, **kwargs)

    def get_type(self):
        class_name = "musicvideo"
        return class_name


class SwgrsPost(models.Model):
    time_stamp = models.IntegerField()
    slug = models.SlugField(unique=True)
    text = models.TextField()
    link_yt = models.CharField(max_length=100, null=True)  # If post has a youtube video that should be embedded
    link_fb = models.CharField(max_length=100, null=True)  # facebook post id
    layout = models.CharField(max_length=30, default='')  # how the post should appear. Select from html presets
    appears = models.ManyToManyField(Character)  # hardcode to swiggers during ingest

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.time_stamp))
        super(SwgrsPost, self).save(*args, **kwargs)

    def get_type(self):
        class_name = "swgrs_post"
        return class_name


class SwgrsMedia(models.Model):
    """Photo or video"""
    time_stamp = models.IntegerField()
    slug = models.SlugField(unique=True)
    text = models.TextField()  # photo description
    photo = models.ImageField(default="swgrs/profile.jpg")  # filename of photo, stored in folder
    video = models.FileField(null=True)  # filename of video, stored in folder
    video_title = models.CharField(max_length=160, null=True)  # title of video
    link_fb = models.CharField(max_length=100, null=True)  # facebook post id
    layout = models.CharField(max_length=30, default='')  # how the post should appear. Select from html presets
    appears = models.ManyToManyField(Character)  # hardcode to swiggers during ingest

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.time_stamp))
        super(SwgrsMedia, self).save(*args, **kwargs)

    def get_type(self):
        class_name = "swgrs_media"
        return class_name

    def is_video(self):
        if self.video:
            return True
        else:
            return False


class SwgrsSong(models.Model):
    alias = models.CharField(max_length=30)
    slug = models.SlugField(unique=True)
    photo = models.ImageField(default="swgrs/profile.jpg")  # filename of photo, stored in folder
    title = models.CharField(max_length=100)
    text = models.TextField()  # description
    sc_embed_code = models.CharField(max_length=100)  # code used for spotify embeds
    link_sc = models.CharField(max_length=100, null=True)  # soundcloud
    appears = models.ManyToManyField(Character, related_name='appears_on_sw_song')  # hardcode to swiggers during ingest

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.title))
        super(SwgrsSong, self).save(*args, **kwargs)

    def get_type(self):
        class_name = "swgrs_song"
        return class_name


class ItemEmbed(models.Model):
    """include another type of item, like person or song"""
    time_stamp = models.IntegerField()
    slug = models.SlugField(unique=True)
    layout = models.CharField(max_length=30, default='standard')  # how the post should appear. Select from html presets
    target = models.CharField(max_length=60)  # alias of item to be embedded. Make this relationship instead
    target_character = models.ManyToManyField(Character)
    target_song = models.ManyToManyField(Song)
    target_album = models.ManyToManyField(Album)
    target_musicvideo = models.ManyToManyField(MusicVideo)
    target_swgrssong = models.ManyToManyField(SwgrsSong)

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.time_stamp))
        super(ItemEmbed, self).save(*args, **kwargs)

    def get_type(self):
        class_name = "itemembed"
        return class_name

    def get_embed(self):
        if self.target_character.all():
            return self.target_character.all().first()
        elif self.target_song.all():
            return self.target_song.all().first()
        elif self.target_album.all():
            return self.target_album.all().first()
        elif self.target_musicvideo.all():
            return self.target_musicvideo.all().first()
        elif self.target_swgrssong.all():
            return self.target_swgrssong.all().first()
        else:
            return None

    def what_kind(self):
        if self.target_character.all():
            return 'character'
        elif self.target_song.all():
            return 'song'
        elif self.target_album.all():
            return 'album'
        elif self.target_musicvideo.all():
            return 'musicvideo'
        elif self.target_swgrssong.all():
            return 'swgrs_song'
        else:
            return None


class Motif(models.Model):
    """Reusable chunks of comment. Formatted as HTML."""
    alias = models.CharField(max_length=30)
    slug = models.SlugField(unique=True)
    text = models.TextField()
    title = models.CharField(max_length=200, default='')
    revision_date = models.DateField()

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.alias))
        self.revision_date = datetime.now()
        super(Motif, self).save(*args, **kwargs)

    def get_type(self):
        class_name = "motif"
        return class_name


class Comment(models.Model):
    """Formatted as HTML."""
    alias = models.CharField(max_length=30)
    slug = models.SlugField(unique=True)
    text = models.TextField()
    author = models.CharField(max_length=200, default='')
    revision_date = models.DateField()
    layout = models.CharField(max_length=30, default='')  # how the post should appear. Select from html presets
    has_motif = models.ManyToManyField(Motif, related_name='in_comment')
    has_motif_open = models.ManyToManyField(Motif, related_name='in_comment_open')
    target = models.CharField(max_length=60)  # alias of item to be embedded. Make this relationship instead
    on_story = models.OneToOneField(Story, null=True, on_delete=models.CASCADE)
    on_profileevent = models.OneToOneField(ProfileEvent, null=True, on_delete=models.CASCADE)
    on_post = models.OneToOneField(Post, null=True, on_delete=models.CASCADE)
    on_postphoto = models.OneToOneField(PostPhoto, null=True, on_delete=models.CASCADE)
    on_postvideo = models.OneToOneField(PostVideo, null=True, on_delete=models.CASCADE)
    on_swgrs_post = models.OneToOneField(SwgrsPost, null=True, on_delete=models.CASCADE)
    on_swgrs_media = models.OneToOneField(SwgrsMedia, null=True, on_delete=models.CASCADE)
    on_character = models.OneToOneField(Character, null=True, on_delete=models.CASCADE)
    on_song = models.OneToOneField(Song, null=True, on_delete=models.CASCADE)
    on_album = models.OneToOneField(Album, null=True, on_delete=models.CASCADE)
    on_musicvideo = models.OneToOneField(MusicVideo, null=True, on_delete=models.CASCADE)
    on_swgrssong = models.OneToOneField(SwgrsSong, null=True, on_delete=models.CASCADE)
    on_itemembed = models.OneToOneField(ItemEmbed, null=True, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.slug = 'comment_' + slugify(str(self.alias))
        self.revision_date = datetime.now()
        super(Comment, self).save(*args, **kwargs)

    def get_type(self):
        class_name = "comment"
        return class_name

    def what_kind(self):
        if self.target_story.all():
            return 'story'
        elif self.target_post.all():
            return 'post'
        elif self.target_postphoto.all():
            return 'postphoto'
        elif self.target_postvideo.all():
            return 'postvideo'
        elif self.target_profileevent.all():
            return 'profileevent'
        elif self.target_swgrspost.all():
            return 'swgrspost'
        elif self.target_swgrsmedia.all():
            return 'swgrsmedia'
        elif self.target_itemembed.all():
            return 'itemembed'
        elif self.target_character.all():
            return 'character'
        elif self.target_song.all():
            return 'song'
        elif self.target_album.all():
            return 'album'
        elif self.target_musicvideo.all():
            return 'musicvideo'
        elif self.target_swgrssong.all():
            return 'swgrs_song'
        else:
            return None


class Hashtag(models.Model):
    name = models.CharField(max_length=200)
    slug = models.CharField(max_length=200)
    tagged_in_post = models.ManyToManyField(Post, related_name='post_hashtag')
    tagged_in_postphoto = models.ManyToManyField(PostPhoto, related_name='photo_hashtag')
    tagged_in_postvideo = models.ManyToManyField(PostVideo, related_name='video_hashtag')
    tagged_in_song = models.ManyToManyField(Song, related_name='song_hashtag')
    tagged_in_album = models.ManyToManyField(Album, related_name='album_hashtag')
    tagged_in_swgrs_song = models.ManyToManyField(SwgrsSong, related_name='swgrs_song_hashtag')
    tagged_in_swgrs_post = models.ManyToManyField(SwgrsPost, related_name='swgrs_post_hashtag')
    tagged_in_swgrs_media = models.ManyToManyField(SwgrsMedia, related_name='swgrs_media_hashtag')
    tagged_in_motif = models.ManyToManyField(Motif, related_name='motif_hashtag')