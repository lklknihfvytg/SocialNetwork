from django.contrib import admin
from django.urls import path, include
from network import views


app_name = 'network'

urlpatterns = [
    path('', views.index, name='index'),
    # path('profile', views.my_profile, name='my_profile'),

    # path('user/<int:user_id>/', views.user_profile_by_id, name='user_profile_by_id'),
    # path('user/<int:user_id>/about', views.user_about, name='user_about'),
    # path('user/<int:user_id>/friends', views.user_friends, name='user_friends'),
    # path('user/<int:user_id>/photos', views.ProfilePhotosView.as_view(), name='user_photos'),
    # path('user/<int:user_id>/videos', views.user_videos, name='user_videos'),

    path('user/<int:user_id>/', views.ProfilePage.as_view(), name='user_profile_by_id'),
    path('user/<int:user_id>/about', views.ProfilePage.as_view(template_name='profile_about.html'), name='user_about'),
    path('user/<int:user_id>/friends', views.ProfilePage.as_view(template_name='profile_friends.html'), name='user_friends'),
    path('user/<int:user_id>/photos', views.ProfilePhotosView.as_view(), name='user_photos'),
    path('user/<int:user_id>/videos', views.ProfilePage.as_view(template_name='profile_videos.html'), name='user_videos'),

    # path('user/<str:username>/', views.user_profile_by_username, name='user_profile_by_username'),
    # path('about', views.about, name='about'),
    path('feed', views.feed, name='feed'),
    path('videos', views.videos, name='videos'),
    path('photos', views.photos, name='photos'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('theme', views.change_theme, name='change_theme'),
    path('friends', views.friends, name='friends'),
    path('search', views.search, name='search'),
    path('upload_photo', views.ProfilePhotosView.as_view(), name='upload_photo'),
    path('follow/<int:user_id>/', views.follow, name='follow'),
    path('unfollow/<int:user_id>/', views.unfollow, name='unfollow'),
]
