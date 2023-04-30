from django import template

from messanger.models import Chat

# from messanger.models import


register = template.Library()


@register.simple_tag
def get_companion(user, chat):
    for u in chat.members.all():
        if u != user:
            return u
    return None


@register.simple_tag
def unreads(user, chat):
    unreads = chat.chat_messages.filter(is_read=False, sender=get_companion(user, chat)).count()
    return str(unreads) if unreads > 0 else ''


@register.simple_tag
def unread_chats(user):
    count = 0
    for chat in user.user_chats.all():
        last = chat.chat_messages.last()
        if last:
            if last.sender != user and not last.is_read:
                count += 1
    return count
