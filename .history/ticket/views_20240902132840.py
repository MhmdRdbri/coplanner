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
        # فقط تیکت‌هایی که کاربر ارسال یا دریافت کرده باشد نمایش داده می‌شود
        return Ticket.objects.filter(sender=user) | Ticket.objects.filter(receiver=user)

    def perform_create(self, serializer):
        # فرستنده به صورت خودکار کاربر وارد شده تنظیم می‌شود
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
        # فقط چت روم‌هایی که کاربر در آن‌ها به عنوان فرستنده یا گیرنده تیکت درگیر است نمایش داده می‌شود
        return ChatRoom.objects.filter(ticket__sender=user) | ChatRoom.objects.filter(ticket__receiver=user)

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # فرستنده به صورت خودکار کاربر وارد شده تنظیم می‌شود
        serializer.save(sender=self.request.user)

    def get_queryset(self):
        user = self.request.user
        # فقط پیام‌هایی که کاربر ارسال کرده یا در چت رومی که او درگیر آن است، قرار دارند نمایش داده می‌شود
        return Message.objects.filter(sender=user) | Message.objects.filter(chatroom__ticket__receiver=user)
