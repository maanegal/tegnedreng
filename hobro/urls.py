from django.urls import path
from . import views

urlpatterns = [
    path('', views.item_list, name='item_list'),
    path('item/<int:pk>/', views.item_detail, name='item_detail'),
    path('song/<int:pk>/', views.song_viewer, name='song_viewer'),
    path('album/<int:pk>/', views.album_viewer, name='album_viewer'),
    path('music/', views.music_list, name='music_list'),
    path('character/<int:pk>/', views.character_viewer, name='character_viewer'),
]