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


class Story(models.Model):
    """Blocks of text describing the story. Formatted as HTML. Timestamps are purely for sorting here"""
    text = models.TextField()
    time_stamp = models.IntegerField()


class Character(models.Model):
    """Information on a character in the story"""
    name = models.CharField(max_length=100)
    photo = models.CharField(max_length=160)  # filename of photo, stored in folder. Maybe change to an image field type?
    text = models.TextField()  # in case a description is needed
    alias = models.CharField(max_length=30)


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


class PostPhoto(models.Model):
    """Photo post items. References a locally stored image. Includes Link items"""
    text = models.TextField()  # photo description
    photo = models.CharField(max_length=160)  # filename of photo, stored in folder. Maybe change to an image field type?
    time_stamp = models.IntegerField()
    page_name = models.CharField(max_length=60)  # link to profile-event via function
    layout = models.CharField(max_length=30, default='standard')  # how the post should appear. Select from html presets
    appears = models.ManyToManyField(Character)  # Set characters that appear in this post
    link_fb = models.CharField(max_length=100, null=True)  # facebook post id
    link_ig = models.CharField(max_length=100, null=True)  # instagram post id
    link_tw = models.CharField(max_length=100, null=True)  # twitter post id


class PostVideo(models.Model):
    """Video post items. References a locally stored video file. Includes Link items"""
    text = models.TextField()  # video description
    video = models.CharField(max_length=160)  # filename of video, stored in folder
    title = models.CharField(max_length=160)  # title of video
    photo = models.CharField(max_length=160)  # filename of photo, stored in folder. Maybe change to an image field type?
    time_stamp = models.IntegerField()
    page_name = models.CharField(max_length=60)  # link to profile-event via function
    layout = models.CharField(max_length=30, default='standard')  # how the post should appear. Select from html presets
    appears = models.ManyToManyField(Character)  # Set characters that appear in this post
    link_fb = models.CharField(max_length=100, null=True)  # facebook post id
    link_ig = models.CharField(max_length=100, null=True)  # instagram post id
    link_tw = models.CharField(max_length=100, null=True)  # twitter post id


class ProfileEvent(models.Model):
    """Posts indicating changes in the online presence, such as new profile picture or page name"""
    time_stamp = models.IntegerField()
    expires = models.IntegerField(null=True)  # one less than value of next object
    page_name = models.CharField(max_length=60)  # link to profile-event via function
    photo = models.CharField(max_length=160)  # filename of photo, stored in folder. Maybe change to an image field type?
    text = models.TextField()  # free text field, in case it is needed
    link_fb = models.CharField(max_length=100, null=True)  # facebook post id
    link_tw = models.CharField(max_length=100, null=True)  # twitter post id


class Album(models.Model):
    """An album, containing songs"""
    alias = models.CharField(max_length=30)
    photo = models.CharField(max_length=160)  # filename of photo, stored in folder. Maybe change to an image field type?
    title = models.CharField(max_length=100)
    text = models.TextField()  # description
    release_date = models.DateField()
    artist_name = models.CharField(max_length=60)  # link to profile-event via function
    embed_url = models.CharField(max_length=100)  # url used embedding item player
    link_yt = models.CharField(max_length=100, null=True)  # youtube
    link_bc = models.CharField(max_length=100, null=True)  # bandcamp
    link_sp = models.CharField(max_length=100, null=True)  # spotify
    link_sc = models.CharField(max_length=100, null=True)  # soundcloud
    link_it = models.CharField(max_length=100, null=True)  # itunes
    # relationship: songs


class ItemEmbed(models.Model):
    """include another type of item, like person or song"""
    time_stamp = models.IntegerField()
    # relationship to another item that will be embedded at timecode


class Song(models.Model):
    """A song. Most belong to an album"""
    alias = models.CharField(max_length=30)
    photo = models.CharField(max_length=160)  # filename of photo, stored in folder. Maybe change to an image field type?
    title = models.CharField(max_length=100)
    track_number = models.IntegerField()
    text = models.TextField()  # description
    artist_name = models.CharField(max_length=60)  # link to profile-event via function
    embed_url = models.CharField(max_length=100)  # url used embedding item player
    link_yt = models.CharField(max_length=100, null=True)  # youtube
    link_bc = models.CharField(max_length=100, null=True)  # bandcamp
    link_sp = models.CharField(max_length=100, null=True)  # spotify
    link_sc = models.CharField(max_length=100, null=True)  # soundcloud
    link_it = models.CharField(max_length=100, null=True)  # itunes
    appears = models.ManyToManyField(Character, related_name='appears_on_song')
    producer = models.ManyToManyField(Character, related_name='produced')
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    # Add lyrics


class MusicVideo(models.Model):
    """An album, containing songs"""
    alias = models.CharField(max_length=30)
    photo = models.CharField(max_length=160)  # filename of photo, stored in folder. Maybe change to an image field type?
    title = models.CharField(max_length=100)
    text = models.TextField()  # description
    release_date = models.DateField()
    artist_name = models.CharField(max_length=60)  # link to profile-event via function
    embed_url = models.CharField(max_length=100)  # url used embedding item player
    link_yt = models.CharField(max_length=100, null=True)  # youtube
    link_bc = models.CharField(max_length=100, null=True)  # bandcamp
    link_sp = models.CharField(max_length=100, null=True)  # spotify
    link_sc = models.CharField(max_length=100, null=True)  # soundcloud
    link_it = models.CharField(max_length=100, null=True)  # itunes
    appears = models.ManyToManyField(Character, related_name='appears_in_video')
    song = models.OneToOneField(Song, on_delete=models.CASCADE)  # The song featured in the music video

