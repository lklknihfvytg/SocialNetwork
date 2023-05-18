from django.shortcuts import render, redirect
from django_registration.forms import User
from .models import Chat, Message
from .forms import MessageForm
from django.views import View
from posts.models import Post


class ChatsView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'login.html')

        rem = []
        chats = Chat.objects.filter(members__in=[request.user])
        for chat in chats:
            if chat.chat_messages.count() == 0:
                rem.append(chat.id)
        chats = chats.exclude(id__in=rem)
        chats = sorted(chats,
                       key=lambda c: c.chat_messages.last().id,
                       reverse=True)
        return render(request, 'messanger.html', {'user': request.user, 'chats': chats})

    def post(self, request):
        if not request.user.is_authenticated:
            return render(request, 'login.html')

        user_id = request.POST['user_id']
        companion = User.objects.get(id=user_id)
        chat = Chat.objects.filter(members__in=[request.user]).filter(members__in=[companion]).distinct().first()
        if not chat:
            chat = Chat.objects.create()
            chat.members.add(request.user)
            chat.members.add(companion)

        return redirect('messanger:messages', chat_id=chat.id)


class MessagesView(View):
    def get(self, request, chat_id):
        if not request.user.is_authenticated:
            return render(request, 'login.html')

        try:
            chat = Chat.objects.get(id=chat_id, members__in=[request.user])
            if chat.chat_messages.count() != 0:
                for message in chat.chat_messages.filter(is_read=False):
                    if message.sender != request.user:
                        message.is_read = True
                        message.save()
        except Chat.DoesNotExist:
            chat = None

        chats = sorted(Chat.objects.filter(members__in=[request.user]),
                       key=lambda c: 999999 if c.chat_messages.count() == 0 else c.chat_messages.last().id,
                       reverse=True)
        context = {
            'user': request.user,
            'chats': chats,
            'main_chat': chat
        }
        return render(request, 'messanger.html', context)

    def post(self, request, chat_id):
        if not request.user.is_authenticated:
            return render(request, 'login.html')

        try:
            redirect_to = request.GET.get('next', '')
        except Exception:
            redirect_to = 'network:feed'

        message_form = MessageForm(request.POST)
        if message_form.is_valid():
            message_form.save()

        return redirect(redirect_to)
