from rest_framework import serializers
from .models import Ticket, ChatRoom, Message

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'title', 'sender', 'receiver', 'description', 'file', 'date_created', 'status']

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'chatroom', 'sender', 'content', 'date_sent']

class ChatRoomSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = ChatRoom
        fields = ['id', 'ticket', 'is_active', 'messages']
