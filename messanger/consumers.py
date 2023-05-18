from datetime import timedelta

from channels.generic.websocket import WebsocketConsumer
from django_registration.forms import User
from messanger.models import Chat, Message
import json


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        user_id = text_data_json['user_id']
        r_type = text_data_json['type']
        opened_chat = text_data_json['opened_chat']
        if opened_chat:
            try:
                chat = Chat.objects.get(id=opened_chat)
                for message in chat.chat_messages.filter(is_read=False):
                    if message.sender.id != user_id:
                        message.is_read = True
                        message.save()
            except Exception:
                print('error')

        if r_type == 'mes' and text_data_json['text']:
            message = Message(sender=User.objects.get(id=user_id), text=text_data_json['text'], chat_id=opened_chat)
            message.save()

        self.send(text_data=chat_serializer(user_id))


class BaseConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        user_id = text_data_json['user_id']
        user = User.objects.get(id=user_id)

        if not user.is_authenticated:
            self.disconnect(0)

        count = 0
        for chat in user.user_chats.all():
            last = chat.chat_messages.last()
            if last:
                if last.sender != user and not last.is_read:
                    count += 1

        self.send(text_data=json.dumps({'count': count}))


def get_companion(chat, user_id):
    for member in chat.members.all():
        if member.id != user_id:
            return member
    return None


def chat_serializer(user_id):
    rem = []
    chats = Chat.objects.filter(members__in=[user_id])
    for chat in chats:
        if chat.chat_messages.count() == 0:
            rem.append(chat.id)
    chats = chats.exclude(id__in=rem)
    chats = sorted(chats, key=lambda c: c.chat_messages.last().id, reverse=True)
    result = []
    for chat in chats:
        messages = chat.chat_messages
        if messages.count() == 0:
            continue
        companion = get_companion(chat, user_id)
        unreads = messages.filter(is_read=False, sender=companion).count()
        mes = [{'position': 'r' if m.sender.id == user_id else 'l', 'text': m.text,
                'is_read': m.is_read, 'time': (m.creation_time+timedelta(hours=3)).strftime('%H:%M')} for m in messages.all().order_by('-id')[:50]]
        result.append({
            'name': f'{companion.profile.name} {companion.profile.surname}',
            'last_message': 'вы: ' + messages.last().text if messages.last().sender.id == user_id else messages.last().text,
            'lm_id': messages.last().id,
            'unreads': unreads,
            'pic': companion.profile.profile_pic.url,
            'chat_id': chat.id,
            'companion_id': companion.id,
            'messages': mes,
            'user_pic': User.objects.get(id=user_id).profile.profile_pic.url
        })
    return json.dumps(result)
