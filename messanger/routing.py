# chat/routing.py
from django.urls import re_path
from . import consumers


websocket_urlpatterns = [
    re_path(r'ws/chats/(?P<username>\w+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/base/(?P<username>\w+)/$', consumers.BaseConsumer.as_asgi()),
]
