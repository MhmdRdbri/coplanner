from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Ticket, Message, ChatRoom
from .serializers import TicketSerializer, MessageSerializer, ChatRoomSerializer

class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # فقط تیکت‌های ارسال‌شده یا دریافت‌شده توسط کاربر را برمی‌گرداند
        return Ticket.objects.filter(sender=user) | Ticket.objects.filter(receiver=user)

    def perform_create(self, serializer):
        # فرستنده را به صورت خودکار تنظیم می‌کند
        serializer.save(sender=self.request.user)

    @action(detail=True, methods=['post'])
    def close(self, request, pk=None):
        ticket = self.get_object()
        ticket.status = 'closed'
        ticket.save()
        chatroom = ChatRoom.objects.get(ticket=ticket)
        chatroom.is_active = False
        chatroom.save()
        return Response({'status': 'chat closed'}, status=status.HTTP_200_OK)

class ChatRoomViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ChatRoomSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # فقط چت روم‌هایی که کاربر در آن‌ها به عنوان فرستنده یا گیرنده تیکت درگیر است را برمی‌گرداند
        return ChatRoom.objects.filter(ticket__sender=user) | ChatRoom.objects.filter(ticket__receiver=user)

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # فرستنده را به صورت خودکار تنظیم می‌کند
        serializer.save(sender=self.request.user)

    def get_queryset(self):
        user = self.request.user
        # فقط پیام‌هایی که کاربر در آن‌ها به عنوان فرستنده یا در چت رومی که کاربر گیرنده آن است، وجود دارند را برمی‌گرداند
        return Message.objects.filter(sender=user) | Message.objects.filter(chatroom__ticket__receiver=user)
