from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.frontpage, name='frontpage'),
    path('kapitel/', views.redirect_chapter, name='redirect_chapter'),
    path('kapitel/alle/', views.item_list, name='item_list'),
    path('kapitel/<int:number>/', views.item_page, name='item_page'),
    path('musik/', views.music_list, name='music_list'),
    path('sang/<slug:slug>/', views.song_viewer, name='song_viewer'),
    path('sang/', views.redirect_music, name='redirect_music'),
    path('album/<slug:slug>/', views.album_viewer, name='album_viewer'),
    path('album/', views.redirect_music, name='redirect_music'),
    path('musikvideo/<slug:slug>/', views.musicvideo_viewer, name='musicvideo_viewer'),
    path('musikvideo/', views.redirect_music, name='redirect_music'),
    path('medlemmer/', views.character_list, name='character_list'),
    path('medlem/', views.redirect_character, name='redirect_character'),
    path('medlem/<slug:slug>/', views.character_viewer, name='character_viewer'),
    path('hashtag/<slug:slug>/', views.hashtag_viewer, name='hashtag_viewer'),
    path('<str:tp>/<int:pk>/', views.item_detail, name='item_detail'),

]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)