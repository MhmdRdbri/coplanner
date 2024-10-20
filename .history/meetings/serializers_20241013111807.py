from rest_framework import serializers
from account.models import CustomUser
from .models import Meeting

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email']

class MeetingSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    participants_ids = serializers.PrimaryKeyRelatedField(
        many=True, write_only=True, queryset=CustomUser.objects.all(), source='participants'
    )

    class Meta:
        model = Meeting
        fields = ['id', 'title', 'meeting_date', 'description', 'participants', 'participants_ids', 'records']