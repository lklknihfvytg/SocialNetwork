from django.contrib import admin
from .models import Chat, Message


class MessageAdmin(admin.ModelAdmin):
    readonly_fields = ['creation_time', 'id']


admin.site.register(Message, MessageAdmin)
admin.site.register(Chat)
