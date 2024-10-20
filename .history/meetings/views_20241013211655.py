from rest_framework import generics, permissions
from .models import Meeting
from .serializers import MeetingSerializer
from account.permissions import HasSpecialAccessPermission, IsAdminOrReadOnly

class MeetingListCreateView(generics.ListCreateAPIView):
    serializer_class = MeetingSerializer
    permission_classes = [HasSpecialAccessPermission, permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.has_special_access:
            # Special users see all meetings
            return Meeting.objects.all() 
        # Regular users only see meetings where they are participants
        return Meeting.objects.filter(participants=user)

    def perform_create(self, serializer):
        user = self.request.user
        if user.has_special_access:
            # Only special users can create meetings
            serializer.save()

class MeetingDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MeetingSerializer
    permission_classes = [HasSpecialAccessPermission, permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.has_special_access:
            # Special users can view all meetings
            return Meeting.objects.all()
        # Regular users can only view meetings where they are participants
        return Meeting.objects.filter(participants=user)

    def perform_update(self, serializer):
        user = self.request.user
        meeting = self.get_object()
        if user.has_special_access:
            # Allow special users to update the meeting, including the 'record' field
            serializer.save()
        else:
            # Regular users cannot modify the 'record' field
            serializer.save(record=meeting.record)  # Preserve the 'record' field as-is