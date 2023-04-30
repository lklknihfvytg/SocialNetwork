from django.shortcuts import render, redirect
from django_registration.forms import User
from messanger.models import Chat, Message
from django.views import View
from posts.models import Post


def show_chats(request):
    if not request.user.is_authenticated:
        return render(request, 'login.html')

    # for chat in chats:
    #     print(chat)
    #     if chat.chat_messages.count() != 0:
    #         print(chat.chat_messages.last().text)

    # pavel = User.objects.get(username='PavelDurov')
    # chat = Chat.objects.get(id=1)
    # for i in range(1, 31):
    #     sender = request.user if (i % 2) == 0 else pavel
    #     message = Message(sender=sender, text=('Привет'+str(i)), chat=chat)
    #     message.save()

    # chats = Chat.objects.filter(members__in=[request.user])
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


def create_chat(request, user_id):
    if not request.user.is_authenticated:
        return render(request, 'login.html')

    companion = User.objects.get(id=user_id)
    chat = Chat.objects.filter(members__in=[request.user]).filter(members__in=[companion]).distinct().first()
    if chat:
        print(chat)
        print('exist')
    else:
        print('dont exist')
        chat = Chat.objects.create()
        chat.members.add(request.user)
        chat.members.add(companion)
    print(chat)
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
        print(chat)
        print(chats)
        return render(request, 'messanger.html', {'user': request.user, 'chats': chats, 'main_chat': chat})

    def post(self, request, chat_id):
        if not request.user.is_authenticated:
            return render(request, 'login.html')

        try:
            redirect_to = request.GET.get('next', '')
        except Exception:
            redirect_to = 'network:feed'

        if request.POST['text']:
            message = Message(sender=request.user, text=request.POST['text'], chat_id=chat_id)
            message.save()
        return redirect(redirect_to)
