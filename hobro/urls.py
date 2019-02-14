from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.item_list, name='item_list'),
    path('sang/<int:pk>/', views.song_viewer, name='song_viewer'),
    path('album/<int:pk>/', views.album_viewer, name='album_viewer'),
    path('musikvideo/<int:pk>/', views.musicvideo_viewer, name='musicvideo_viewer'),
    path('musik/', views.music_list, name='music_list'),
    path('medlem/<int:pk>/', views.character_viewer, name='character_viewer'),
    path('hashtag/<int:pk>/', views.hashtag_viewer, name='hashtag_viewer'),
    path('<str:tp>/<int:pk>/', views.item_detail, name='item_detail'),

]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)