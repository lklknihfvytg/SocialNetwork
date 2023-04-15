from django.contrib.auth.models import User
from django.db import models


class Chat(models.Model):
    members = models.ManyToManyField(User)


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_messages')
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='chat_messages')
    text = models.CharField(max_length=1280)
    creation_time = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['creation_time']

    def __str__(self):
        return self.text
