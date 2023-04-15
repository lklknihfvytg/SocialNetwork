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

    chats = Chat.objects.filter(members__in=[request.user])
    return render(request, 'messanger.html', {'user': request.user, 'chats': chats})


def create_chat(request, user_id):
    try:
        chat = Chat.objects.filter(members__in=[request.user.id, user_id]).distinct().first()
        print('exist')
    except Exception:
        print('dont exist')
        chat = Chat.objects.create()
        chat.members.add(request.user)
        chat.members.add(user_id)

    return redirect('messanger:messages', chat_id=chat.id)


class MessagesView(View):
    def get(self, request, chat_id):
        try:
            chat = Chat.objects.get(id=chat_id, members__in=[request.user])
            if chat.chat_messages.count() != 0:
                for message in chat.chat_messages.filter(is_read=False):
                    if message.sender != request.user:
                        message.is_read = True
                        message.save()
            else:
                chat = None
        except Chat.DoesNotExist:
            chat = None

        chats = Chat.objects.filter(members__in=[request.user])
        return render(request, 'messanger.html', {'user': request.user, 'chats': chats, 'main_chat': chat})

    def post(self, request, chat_id):
        try:
            redirect_to = request.GET.get('next', '')
        except Exception:
            redirect_to = 'network:feed'

        if request.POST['text']:
            message = Message(sender=request.user, text=request.POST['text'], chat_id=chat_id)
            message.save()
        return redirect(redirect_to)