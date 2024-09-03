from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Ticket, ChatRoom, Message
from .serializers import TicketSerializer, ChatRoomSerializer, MessageSerializer

class CreateTicketAPIView(generics.CreateAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        sender = self.request.user
        receiver = serializer.validated_data['receiver']
        
        # Check if there's an existing chatroom for this pair
        existing_chatroom = ChatRoom.objects.filter(ticket__sender=sender, ticket__receiver=receiver, is_active=True).first()
        if existing_chatroom:
            raise serializers.ValidationError("There is already an active chatroom between these users.")

        # Create the ticket and chatroom
        ticket = serializer.save(sender=sender)
        ChatRoom.objects.create(ticket=ticket)

class ChatRoomListAPIView(generics.ListAPIView):
    serializer_class = ChatRoomSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ChatRoom.objects.filter(ticket__sender=user) | ChatRoom.objects.filter(ticket__receiver=user)

class SendMessageAPIView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        chatroom = get_object_or_404(ChatRoom, id=self.kwargs['chatroom_id'], is_active=True)
        if chatroom.ticket.receiver != self.request.user and chatroom.ticket.sender != self.request.user:
            raise serializers.ValidationError("You are not allowed to send messages in this chatroom.")
        serializer.save(sender=self.request.user, chatroom=chatroom)

        # Update ticket status
        if chatroom.ticket.status == 'sent':
            chatroom.ticket.status = 'in_process'
            chatroom.ticket.save()

class CloseTicketAPIView(generics.UpdateAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        ticket = get_object_or_404(Ticket, id=self.kwargs['ticket_id'])
        if ticket.sender != request.user:
            return Response({"detail": "You do not have permission to close this ticket."}, status=status.HTTP_403_FORBIDDEN)
        
        ticket.status = 'closed'
        ticket.save()

        chatroom = ticket.chatroom
        chatroom.is_active = False
        chatroom.save()

        return Response({"detail": "Ticket and associated chatroom closed."}, status=status.HTTP_200_OK)

class TicketListAPIView(generics.ListAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Ticket.objects.filter(sender=user) | Ticket.objects.filter(receiver=user)
