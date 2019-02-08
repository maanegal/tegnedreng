from django.db import models


# Sections in the story. Plain text, renders to HTML headings H2. Timestamps are purely for sorting here
class Section(models.Model):
    text = models.CharField(max_length=200)
    time_stamp = models.IntegerField()

    def publish(self):
        self.save()

    def __str__(self):
        return str(self.time_stamp)


# Blocks of text describing the story. Formatted as HTML. Timestamps are purely for sorting here
class Story(models.Model):
    text = models.TextField()
    time_stamp = models.IntegerField()

    def publish(self):
        self.save()

    def __str__(self):
        return str(self.time_stamp)


class Post(models.Model):
    text = models.TextField()
    time_stamp = models.IntegerField()
    page_name = models.CharField(max_length=100)
