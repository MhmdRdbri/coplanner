from rest_framework import serializers
from .models import Ticket, Message, ChatRoom

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'title', 'sender', 'receiver', 'description', 'file', 'date', 'status']

class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = ['id', 'ticket', 'is_active']

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'chatroom', 'sender', 'text', 'file', 'timestamp']
