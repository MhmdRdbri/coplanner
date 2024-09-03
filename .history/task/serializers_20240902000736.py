from rest_framework import serializers
from .models import Ticket, ChatRoom, ChatMessage
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class ChatMessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = ChatMessage
        fields = ['id', 'sender', 'message', 'created_at']

class ChatRoomSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = ChatMessageSerializer(many=True, read_only=True)

    class Meta:
        model = ChatRoom
        fields = ['id', 'participants', 'created_at', 'is_active', 'messages']

class TicketSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)
    chat_room = ChatRoomSerializer(read_only=True)

    class Meta:
        model = Ticket
        fields = ['id', 'title', 'description', 'sender', 'receiver', 'chat_room', 'status', 'created_at', 'updated_at']

    def create(self, validated_data):
        request = self.context.get('request')
        sender = request.user
        receiver_id = self.context['receiver_id']
        receiver = User.objects.get(id=receiver_id)

        # یافتن یا ایجاد یک ChatRoom جدید
        chat_room, created = ChatRoom.objects.get_or_create(
            participants__in=[sender, receiver],
            is_active=True
        )

        if created:
            chat_room.participants.add(sender, receiver)

        ticket = Ticket.objects.create(
            title=validated_data['title'],
            description=validated_data['description'],
            sender=sender,
            receiver=receiver,
            chat_room=chat_room,
            status='sent'
        )

        return ticket
