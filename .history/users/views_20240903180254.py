from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from account.models import CustomUser, Profile
from .serializers import UserSerializer, ProfileSerializer
from account.permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from .permissions import IsOwnerOrAdmin
from rest_framework.exceptions import PermissionDenied

class ProfileListView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [AllowAny]  # Any user can view profiles

class ProfileDetailView(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [AllowAny]  # Any user can view profiles

class ProfileUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]  # Only owners or admins can update
    
class ProfileUserUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]  # Only owners or admins can update

    def get_object(self):
        return self.request.user.profile


class UserDeleteView(generics.DestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def perform_destroy(self, instance):
        if not self.request.user.has_special_access:
            raise PermissionDenied("You do not have permission to delete this user.")
        profile = instance.profile
        if profile:
            profile.delete()

        instance.delete()