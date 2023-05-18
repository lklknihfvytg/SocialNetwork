from django import forms
from .models import Chat, Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('sender', 'text', 'chat')
