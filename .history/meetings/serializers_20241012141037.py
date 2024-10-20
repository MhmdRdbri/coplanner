from rest_framework import serializers
from account.models import User
from .models import Meeting

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class MeetingSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    participants_ids = serializers.PrimaryKeyRelatedField(
        many=True, write_only=True, queryset=User.objects.all(), source='participants'
    )

    class Meta:
        model = Meeting
        fields = ['id', 'title', 'meeting_date', 'description', 'participants', 'participants_ids', 'records']