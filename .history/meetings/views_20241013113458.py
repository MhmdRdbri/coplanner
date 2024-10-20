from rest_framework import generics, permissions
from .models import Meeting
from .serializers import MeetingSerializer
from account.permissions import HasSpecialAccessPermission, IsAdminOrReadOnly

class MeetingListCreateView(generics.ListCreateAPIView):
    serializer_class = MeetingSerializer
    # permission_classes = [HasSpecialAccessPermission]

    def get_queryset(self):
        user = self.request.user
        if user.has_special_access:
            return Meeting.objects.all() 
        return Meeting.objects.filter(participants=user) 

    def perform_create(self, serializer):
        serializer.save()  # Customize create if needed


class MeetingDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MeetingSerializer
    permission_classes = [HasSpecialAccessPermission]

    def get_queryset(self):
        user = self.request.user
        if user.has_special_access:
            return Meeting.objects.all()
        return Meeting.objects.filter(participants=user)  
