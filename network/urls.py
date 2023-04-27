from django.contrib import admin
from django.urls import path, include
from network import views


app_name = 'network'

urlpatterns = [
    path('', views.index, name='index'),
    path('profile', views.my_profile, name='my_profile'),
    path('user/<int:user_id>/', views.user_profile_by_id, name='user_profile_by_id'),
    path('user/<str:username>/', views.user_profile_by_username, name='user_profile_by_username'),
    path('about', views.about, name='about'),
    path('feed', views.feed, name='feed'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('theme', views.change_theme, name='change_theme'),
    # path('receipt/', views.receipt, name='receipt'),
    # path('receipt_done/', views.receipt_done, name='receipt_done'),
    # path('receipt_add/', views.receipt_add, name='receipt_add'),
    # path('table/', views.table, name='table'),
]