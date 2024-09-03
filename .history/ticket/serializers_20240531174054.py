from rest_framework import serializers
from .models import Ticket, Attachment, Response

class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ['file', 'uploaded_at']

class ResponseSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Response
        fields = ['id', 'ticket', 'user', 'message', 'created_at']

class TicketSerializer(serializers.ModelSerializer):
    attachments = AttachmentSerializer(many=True, read_only=True)
    responses = ResponseSerializer(many=True, read_only=True)

    class Meta:
        model = Ticket
        fields = ['id', 'user', 'admin', 'subject', 'message', 'status', 'attachments', 'responses', 'created_at', 'updated_at']

class TicketCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['subject', 'message']

class TicketUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['status']

class ResponseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = ['message']