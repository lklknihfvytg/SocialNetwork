from django.contrib import admin
from django.urls import path, include
from messanger import views


app_name = 'messanger'

urlpatterns = [
    path('', views.show_chats, name='show_chats'),
    path('create/<int:user_id>/', views.create_chat, name='create_chat'),
    path('<int:chat_id>/', views.MessagesView.as_view(), name='messages'),
]
