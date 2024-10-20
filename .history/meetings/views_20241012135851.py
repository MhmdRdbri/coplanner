from rest_framework import generics, permissions
from .models import Meeting
from .serializers import MeetingSerializer
from account.permissions import HasSpecialAccessPermission, IsAdminOrReadOnly

class MeetingListCreateView(generics.ListCreateAPIView):
    serializer_class = MeetingSerializer
    permission_classes = [HasSpecialAccessPermission]

    def get_queryset(self):
        user = self.request.user
        # Show meetings where the user is a participant or has special access
        if user.has_special_access:
            return Meeting.objects.all()  # Special access: see all meetings
        return Meeting.objects.filter(participants=user)  # Filter meetings where user is a participant

    def perform_create(self, serializer):
        serializer.save()  # Customize create if needed


class MeetingDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MeetingSerializer
    permission_classes = [HasSpecialAccessPermission]

    def get_queryset(self):
        user = self.request.user
        # Show only the meetings where the user is a participant or has special access
        if user.has_special_access:
            return Meeting.objects.all()  # Special access: access all meetings
        return Meeting.objects.filter(participants=user)  # Filter meetings where user is a participant
