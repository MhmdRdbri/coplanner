from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Meeting
from .serializers import MeetingSerializer

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
        else:
            # Regular users cannot create meetings
            raise PermissionDenied("You do not have permission to create meetings.")

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

    def perform_update(self, serializer):
        user = self.request.user
        if user.has_special_access:
            # Allow special users to update all meeting fields
            serializer.save()
        else:
            # Regular users cannot update meetings
            raise PermissionDenied("You do not have permission to update meetings.")

    def destroy(self, request, *args, **kwargs):
        user = self.request.user
        if user.has_special_access:
            # Special users can delete meetings
            return super().destroy(request, *args, **kwargs)
        else:
            # Regular users cannot delete meetings
            return Response(
                {"detail": "You do not have permission to delete this meeting."},
                status=status.HTTP_403_FORBIDDEN
            )
