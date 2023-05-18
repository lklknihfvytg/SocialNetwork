from django.contrib import admin
from django.urls import path, include
from messanger import views


app_name = 'messanger'

urlpatterns = [
    path('', views.ChatsView.as_view(), name='show_chats'),
    path('create_chat/', views.ChatsView.as_view(), name='create_chat'),
    path('<int:chat_id>/', views.MessagesView.as_view(), name='messages'),
]
