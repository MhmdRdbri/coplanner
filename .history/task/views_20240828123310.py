from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status as drf_status
from .models import Task
from .serializers import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Filter tasks where the user is either the sender or the receiver
        return Task.objects.filter(models.Q(sender=user) | models.Q(receiver=user))

    def perform_create(self, serializer):
        # Automatically set the sender to the currently authenticated user
        serializer.save(sender=self.request.user)

    def update(self, request, *args, **kwargs):
        # Ensure that only the receiver can update the task status
        task = self.get_object()

        if request.user != task.receiver:
            return Response({"detail": "You do not have permission to change the status of this task."},
                            status=drf_status.HTTP_403_FORBIDDEN)

        return super().update(request, *args, **kwargs)
