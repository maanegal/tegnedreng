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

# class: Character


# POST ELEMENTS

class Post(models.Model):
    """Basic post items. Includes Link items"""
    text = models.TextField()
    time_stamp = models.IntegerField()
    page_name = models.CharField(max_length=100)

# class: PostPhoto
# class: PostVideo
# class: ProfileEvent
# class: ItemEmbed -- include another type of item, like person or song

# MUSIC
# class: Song
# class: Album
# class: Video
