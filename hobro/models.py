from django.db import models


# BASIC STORY ELEMENTS

class Section(models.Model):
    """Sections in the story. Plain text, renders to HTML headings H2. Timestamps are purely for sorting here"""
    text = models.CharField(max_length=200)
    time_stamp = models.IntegerField()

    def publish(self):
        self.save()

    def __str__(self):
        return str(self.time_stamp)


class Story(models.Model):
    """Blocks of text describing the story. Formatted as HTML. Timestamps are purely for sorting here"""
    text = models.TextField()
    time_stamp = models.IntegerField()

    def publish(self):
        self.save()

    def __str__(self):
        return str(self.time_stamp)


class Character(models.Model):
    """Information on a character in the story"""
    name = models.CharField(max_length=100)
    photo = models.CharField(max_length=160)  # filename of photo, stored in folder. Maybe change to an image field type?
    text = models.TextField()  # in case a description is needed
    alias = models.CharField(max_length=30)
    # set relationships


# POST ELEMENTS
class Post(models.Model):
    """Basic post items. Includes Link items"""
    text = models.TextField()
    time_stamp = models.IntegerField()
    page_name = models.CharField(max_length=60)  # link to profile-event via function
    layout = models.CharField(max_length=30)  # how the post should appear. Select from html presets
    link_fb = models.CharField(max_length=100)  # facebook post id
    link_tw = models.CharField(max_length=100)  # twitter post id


class PostPhoto(models.Model):
    """Photo post items. References a locally stored image. Includes Link items"""
    text = models.TextField()  # photo description
    photo = models.CharField(max_length=160)  # filename of photo, stored in folder. Maybe change to an image field type?
    time_stamp = models.IntegerField()
    page_name = models.CharField(max_length=60)  # link to profile-event via function
    layout = models.CharField(max_length=30)  # how the post should appear. Select from html presets
    link_fb = models.CharField(max_length=100)  # facebook post id
    link_ig = models.CharField(max_length=100)  # instagram post id
    link_tw = models.CharField(max_length=100)  # twitter post id


class PostVideo(models.Model):
    """Video post items. References a locally stored video file. Includes Link items"""
    text = models.TextField()  # video description
    video = models.CharField(max_length=160)  # filename of video, stored in folder
    title = models.CharField(max_length=160)  # title of video
    thumb = models.CharField(max_length=160)  # filename of photo, stored in folder. Maybe change to an image field type?
    time_stamp = models.IntegerField()
    page_name = models.CharField(max_length=60)  # link to profile-event via function
    layout = models.CharField(max_length=30)  # how the post should appear. Select from html presets
    link_fb = models.CharField(max_length=100)  # facebook post id
    link_ig = models.CharField(max_length=100)  # instagram post id
    link_tw = models.CharField(max_length=100)  # twitter post id


class ProfileEvent(models.Model):
    """Posts indicating changes in the online presence, such as new profile picture or page name"""
    time_stamp = models.IntegerField()
    page_name = models.CharField(max_length=60)  # link to profile-event via function
    photo = models.CharField(max_length=160)  # filename of photo, stored in folder. Maybe change to an image field type?
    text = models.TextField()  # free text field, in case it is needed
    link_fb = models.CharField(max_length=100)  # facebook post id
    link_tw = models.CharField(max_length=100)  # twitter post id


class ItemEmbed(models.Model):
    """include another type of item, like person or song"""
    time_stamp = models.IntegerField()
    # relationship to another item

# MUSIC
# class: Song
# class: Album
# class: Video
