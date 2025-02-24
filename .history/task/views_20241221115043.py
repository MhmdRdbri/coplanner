from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status as drf_status
from .models import Task
from .serializers import TaskSerializer
from django.db import models
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from account.permissions import HasSpecialAccessPermission

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [HasSpecialAccessPermission]

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(models.Q(sender=user) | models.Q(receiver=user))

    def update(self, request, *args, **kwargs):
        task = self.get_object()

        # Check if the user is the sender of the task
        if request.user != task.sender:
            return Response(
                {"error": "You do not have permission to edit this task."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Allow the update if the user is the sender
        return super().update(request, *args, **kwargs)

    @action(detail=True, methods=['post'])
    def mark_as_done(self, request, pk=None):
        task = self.get_object()

        # Ensure that only the receiver or sender can mark the task as done
        if request.user == task.receiver or request.user == task.sender:
            task.status = 'done'
            task.save()
            return Response({"status": "Task marked as done."}, status=status.HTTP_200_OK)
        return Response({"error": "You do not have permission to mark this task as done."}, status=status.HTTP_403_FORBIDDEN)