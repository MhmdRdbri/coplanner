from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Meeting
from .serializers import MeetingSerializer
from account.permissions import HasSpecialAccessPermission, IsAdminOrReadOnly

class MeetingListCreateView(generics.ListCreateAPIView):
    serializer_class = MeetingSerializer
    permission_classes = [permissions.IsAuthenticated]

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
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {"detail": "You do not have permission to create meetings."},
                status=status.HTTP_403_FORBIDDEN
            )

class MeetingDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MeetingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.has_special_access:
            # Special users can view all meetings
            return Meeting.objects.all()
        # Regular users can only view meetings where they are participants
        return Meeting.objects.filter(participants=user)

    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except Meeting.DoesNotExist:
            return Response(
                {"detail": "Meeting not found or access is forbidden."},
                status=status.HTTP_404_NOT_FOUND
            )

    def perform_update(self, serializer):
        user = self.request.user
        meeting = self.get_object()
        if user.has_special_access:
            # Allow special users to update the meeting, including the 'record' field
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # Regular users cannot modify the 'record' field
            serializer.save(record=meeting.record)  # Preserve the 'record' field as-is
            return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        user = self.request.user
        meeting = self.get_object()

        if user.has_special_access:
            self.perform_destroy(meeting)
            return Response(
                {"detail": "Meeting deleted successfully."},
                status=status.HTTP_204_NO_CONTENT
            )
        else:
            return Response(
                {"detail": "You do not have permission to delete this meeting."},
                status=status.HTTP_403_FORBIDDEN
            )