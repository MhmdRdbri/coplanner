from rest_framework import viewsets, status
from rest_framework.response import Response as DRFResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .models import Ticket, Attachment, Response
from .serializers import TicketSerializer, TicketCreateSerializer, TicketUpdateSerializer, AttachmentSerializer, ResponseSerializer, ResponseCreateSerializer

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return TicketCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return TicketUpdateSerializer
        return TicketSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Ticket.objects.all()
        return Ticket.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'], url_path='add-attachment')
    def add_attachment(self, request, pk=None):
        ticket = self.get_object()
        file = request.FILES.get('file')
        if file:
            Attachment.objects.create(ticket=ticket, file=file)
            return DRFResponse({'status': 'attachment added'}, status=status.HTTP_201_CREATED)
        return DRFResponse({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def mark_as_read(self, request, pk=None):
        ticket = self.get_object()
        if request.user.is_staff:
            ticket.status = 'read'
            ticket.save()
            return DRFResponse({'status': 'ticket marked as read'})
        return DRFResponse({'error': 'Only admin can mark as read'}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=['post'], url_path='respond')
    def respond(self, request, pk=None):
        ticket = self.get_object()
        if not request.user.is_staff:
            return DRFResponse({'error': 'Only admin can respond'}, status=status.HTTP_403_FORBIDDEN)

        serializer = ResponseCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, ticket=ticket)
            return DRFResponse(serializer.data, status=status.HTTP_201_CREATED)
        return DRFResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)