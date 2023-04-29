from django.contrib import admin
from django.urls import path, include
from posts import views


app_name = 'posts'

urlpatterns = [
    path('post_like/', views.post_like, name='post_like'),
    path('post/<int:post_id>/', views.post_by_id, name='post_by_id'),
    path('create_post', views.create_post, name='create_post')
]