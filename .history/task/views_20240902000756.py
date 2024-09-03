from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Ticket, ChatRoom, ChatMessage

class CreateTicketAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        title = request.data.get('title')
        description = request.data.get('description')
        receiver_id = request.data.get('receiver_id')

        if not title or not description or not receiver_id:
            return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

        receiver = User.objects.get(id=receiver_id)
        sender = request.user

        # بررسی اینکه آیا چت فعالی با این کاربر وجود دارد
        chat_room, created = ChatRoom.objects.get_or_create(
            participants__in=[sender, receiver],
            is_active=True
        )

        if created:
            chat_room.participants.add(sender, receiver)

        ticket = Ticket.objects.create(
            title=title,
            description=description,
            sender=sender,
            receiver=receiver,
            chat_room=chat_room,
        )

        return Response({"message": "Ticket created successfully."}, status=status.HTTP_201_CREATED)

class SendMessageAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, chat_room_id):
        try:
            chat_room = ChatRoom.objects.get(id=chat_room_id)

            if not chat_room.is_active:
                return Response({"error": "This chat room is closed."}, status=status.HTTP_403_FORBIDDEN)

            message_text = request.data.get('message')

            if not message_text:
                return Response({"error": "Message text is required."}, status=status.HTTP_400_BAD_REQUEST)

            message = ChatMessage.objects.create(
                chat_room=chat_room,
                sender=request.user,
                message=message_text
            )

            # به روزرسانی وضعیت تیکت
            ticket = Ticket.objects.filter(chat_room=chat_room).first()
            ticket.update_status(user=request.user)

            return Response({"message": "Message sent successfully."}, status=status.HTTP_201_CREATED)

        except ChatRoom.DoesNotExist:
            return Response({"error": "Chat room not found."}, status=status.HTTP_404_NOT_FOUND)

class CloseTicketAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, ticket_id):
        try:
            ticket = Ticket.objects.get(id=ticket_id)

            if request.user != ticket.sender and request.user != ticket.receiver:
                return Response({"error": "You do not have permission to close this ticket."},
                                status=status.HTTP_403_FORBIDDEN)

            ticket.status = 'closed'
            ticket.save()

            chat_room = ticket.chat_room
            chat_room.is_active = False
            chat_room.save()

            return Response({"message": "Ticket and chat room closed successfully."}, status=status.HTTP_200_OK)

        except Ticket.DoesNotExist:
            return Response({"error": "Ticket not found."}, status=status.HTTP_404_NOT_FOUND)
