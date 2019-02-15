from django.db import models


# BASIC STORY ELEMENTS
class Section(models.Model):
    """Sections in the story. Plain text, renders to HTML headings H2. Timestamps are purely for sorting here"""
    text = models.CharField(max_length=200)
    time_stamp = models.IntegerField()
    expires = models.IntegerField(null=True)  # one less than value of next object

    '''def publish(self):
        self.save()

    def __str__(self):
        return str(self.time_stamp)'''

    def get_type(self):
        class_name = "section"
        return class_name


class Story(models.Model):
    """Blocks of text describing the story. Formatted as HTML. Timestamps are purely for sorting here"""
    text = models.TextField()
    time_stamp = models.IntegerField()

    def get_type(self):
        class_name = "story"
        return class_name


class Character(models.Model):
    """Information on a character in the story"""
    name = models.CharField(max_length=100)
    photo = models.ImageField(default="default.jpg")  # filename of photo, stored in folder
    text = models.TextField()  # in case a description is needed
    alias = models.CharField(max_length=30)

    def get_type(self):
        class_name = "character"
        return class_name


# POST ELEMENTS
class Post(models.Model):
    """Basic post items. Includes Link items"""
    text = models.TextField()
    time_stamp = models.IntegerField()
    page_name = models.CharField(max_length=60)  # link to profile-event via function
    layout = models.CharField(max_length=30, default='standard')  # how the post should appear. Select from html presets
    appears = models.ManyToManyField(Character) # Set characters that appear in this post
    link_fb = models.CharField(max_length=100, null=True)  # facebook post id
    link_tw = models.CharField(max_length=100, null=True)  # twitter post id

    def get_type(self):
        class_name = "post"
        return class_name


class PostPhoto(models.Model):
    """Photo post items. References a locally stored image. Includes Link items"""
    text = models.TextField()  # photo description
    photo = models.ImageField(default="default.jpg")  # filename of photo, stored in folder
    time_stamp = models.IntegerField()
    page_name = models.CharField(max_length=60)  # link to profile-event via function
    layout = models.CharField(max_length=30, default='standard')  # how the post should appear. Select from html presets
    appears = models.ManyToManyField(Character)  # Set characters that appear in this post
    link_fb = models.CharField(max_length=100, null=True)  # facebook post id
    link_ig = models.CharField(max_length=100, null=True)  # instagram post id
    link_tw = models.CharField(max_length=100, null=True)  # twitter post id

    def get_type(self):
        class_name = "postphoto"
        return class_name


class PostVideo(models.Model):
    """Video post items. References a locally stored video file. Includes Link items"""
    text = models.TextField()  # video description
    video = models.FileField()  # filename of video, stored in folder
    title = models.CharField(max_length=160, null=True)  # title of video
    photo = models.ImageField(default="default.jpg")  # filename of photo, stored in folder
    time_stamp = models.IntegerField()
    page_name = models.CharField(max_length=60)  # link to profile-event via function
    layout = models.CharField(max_length=30, default='standard')  # how the post should appear. Select from html presets
    appears = models.ManyToManyField(Character)  # Set characters that appear in this post
    link_fb = models.CharField(max_length=100, null=True)  # facebook post id
    link_ig = models.CharField(max_length=100, null=True)  # instagram post id
    link_tw = models.CharField(max_length=100, null=True)  # twitter post id

    def get_type(self):
        class_name = "postvideo"
        return class_name


class ProfileEvent(models.Model):
    """Posts indicating changes in the online presence, such as new profile picture or page name"""
    time_stamp = models.IntegerField()
    expires = models.IntegerField(null=True)  # one less than value of next object
    page_name = models.CharField(max_length=60)  # link to profile-event via function
    photo = models.ImageField(default="default.jpg")  # filename of photo, stored in folder
    text = models.TextField()  # free text field, in case it is needed
    link_fb = models.CharField(max_length=100, null=True)  # facebook post id
    link_tw = models.CharField(max_length=100, null=True)  # twitter post id

    def get_type(self):
        class_name = "profileevent"
        return class_name


class Album(models.Model):
    """An album, containing songs"""
    alias = models.CharField(max_length=30)
    photo = models.ImageField(default="default.jpg")  # filename of photo, stored in folder
    title = models.CharField(max_length=100)
    text = models.TextField()  # description
    release_date = models.DateField()
    artist_name = models.CharField(max_length=60)  # link to profile-event via function
    bc_embed_code = models.CharField(max_length=100)  # code used for bandcamp embeds
    sp_embed_code = models.CharField(max_length=100, null=True)  # code used for spotify embeds
    link_yt = models.CharField(max_length=100, null=True)  # youtube
    link_bc = models.CharField(max_length=100, null=True)  # bandcamp
    link_sp = models.CharField(max_length=100, null=True)  # spotify
    link_sc = models.CharField(max_length=100, null=True)  # soundcloud
    link_it = models.CharField(max_length=100, null=True)  # itunes
    # relationship: songs

    def get_type(self):
        class_name = "album"
        return class_name


class Song(models.Model):
    """A song. Most belong to an album"""
    alias = models.CharField(max_length=30)
    photo = models.ImageField(default="default.jpg")  # filename of photo, stored in folder
    title = models.CharField(max_length=100)
    track_number = models.IntegerField(null=True)
    text = models.TextField()  # description
    artist_name = models.CharField(max_length=60)  # link to profile-event via function
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
    # Add lyrics

    def get_type(self):
        class_name = "song"
        return class_name


class MusicVideo(models.Model):
    """An album, containing songs"""
    alias = models.CharField(max_length=30)
    title = models.CharField(max_length=100)
    text = models.TextField()  # description
    release_date = models.DateField(null=True)
    artist_name = models.CharField(max_length=60)  # link to profile-event via function
    embed_url = models.CharField(max_length=100)  # url used embedding item player
    link_yt = models.CharField(max_length=100, null=True)  # youtube
    link_bc = models.CharField(max_length=100, null=True)  # bandcamp
    link_sp = models.CharField(max_length=100, null=True)  # spotify
    link_sc = models.CharField(max_length=100, null=True)  # soundcloud
    link_it = models.CharField(max_length=100, null=True)  # itunes
    appears = models.ManyToManyField(Character, related_name='appears_in_video')
    song = models.OneToOneField(Song, null=True, on_delete=models.CASCADE)  # The song featured in the music video

    def get_type(self):
        class_name = "musicvideo"
        return class_name


class SwgrsPost(models.Model):
    text = models.TextField()
    text_link = models.CharField(max_length=100, null=True)  # If post has a content link
    time_stamp = models.IntegerField()
    layout = models.CharField(max_length=30, default='standard')  # how the post should appear. Select from html presets
    link_fb = models.CharField(max_length=100, null=True)  # facebook post id

    def get_type(self):
        class_name = "swgrs_post"
        return class_name


class SwgrsMedia(models.Model):
    """Photo or video"""
    text = models.TextField()  # photo description
    photo = models.ImageField(default="swgrs/profile.jpg")  # filename of photo, stored in folder
    video = models.FileField(null=True)  # filename of video, stored in folder
    video_title = models.CharField(max_length=160, null=True)  # title of video
    time_stamp = models.IntegerField()
    layout = models.CharField(max_length=30, default='standard')  # how the post should appear. Select from html presets
    link_fb = models.CharField(max_length=100, null=True)  # facebook post id

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
    photo = models.ImageField(default="swgrs/profile.jpg")  # filename of photo, stored in folder
    title = models.CharField(max_length=100)
    text = models.TextField()  # description
    sc_embed_code = models.CharField(max_length=100)  # code used for spotify embeds
    link_sc = models.CharField(max_length=100, null=True)  # soundcloud

    def get_type(self):
        class_name = "swgrs_song"
        return class_name


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


class ItemEmbed(models.Model):
    """include another type of item, like person or song"""
    time_stamp = models.IntegerField()
    target = models.CharField(max_length=60)  # alias of item to be embedded. Make this relationship instead
    target_character = models.ManyToManyField(Character)
    target_song = models.ManyToManyField(Song)
    target_album = models.ManyToManyField(Album)
    target_musicvideo = models.ManyToManyField(MusicVideo)
    # relationship to another item that will be embedded at timecode

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
        else:
            return None