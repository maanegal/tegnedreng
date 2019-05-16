from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import *


class StaticViewSitemap(Sitemap):
    priority = 1

    def items(self):
        x = ['frontpage', 'about', 'search_index', 'photo_gallery', 'music_list', 'character_list', 'hashtag_list']
        return x

    def location(self, item):
        return reverse(item)


class ChapterSitemap(Sitemap):
    priority = 0.9

    def items(self):
        return ['item_page']

    def location(self, item):
        return reverse(item, args=[1])


class SongSitemap(Sitemap):
    priority = 0.9

    def items(self):
        return Song.objects.all()


class AlbumSitemap(Sitemap):
    priority = 0.8

    def items(self):
        return Album.objects.all()


class MusicvideoSitemap(Sitemap):
    priority = 0.9

    def items(self):
        return MusicVideo.objects.all()


class SwSongSitemap(Sitemap):
    priority = 0.5

    def items(self):
        return SwgrsSong.objects.all()


class CharacterSitemap(Sitemap):
    priority = 0.5

    def items(self):
        return Character.objects.all()


class HashtagSitemap(Sitemap):
    priority = 0.3

    def items(self):
        return Hashtag.objects.all()