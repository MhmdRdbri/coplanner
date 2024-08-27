from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Task
from .serializers import TaskSerializer, SubTaskSerializer
from account.permissions import IsAdminOrHasSpecialAccessOrOwner

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAdminOrHasSpecialAccessOrOwner]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.has_special_access:
            return Task.objects.all()
        return Task.objects.filter(user=user)

    def perform_create(self, serializer):
        if self.request.user.is_staff or self.request.user.has_special_access:
            serializer.save()
        else:
            serializer.save(user=self.request.user)

    @action(detail=True, methods=['patch'])
    def update_task(self, request, pk=None):
        task = self.get_object()
        self.check_object_permissions(request, task)
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def delete_task(self, request, pk=None):
        task = self.get_object()
        self.check_object_permissions(request, task)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class SubTaskViewSet(viewsets.ModelViewSet):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer
    permission_classes = [IsAdminOrHasSpecialAccessOrOwner]

    def get_queryset(self):
        task_id = self.request.query_params.get('task', None)
        queryset = SubTask.objects.all()
        if task_id:
            queryset = queryset.filter(task_id=task_id)
        
        user = self.request.user
        if user.is_staff or user.has_special_access:
            return queryset
        return queryset.filter(task__user=user)

    @action(detail=True, methods=['patch'])
    def update_subtask(self, request, pk=None):
        subtask = self.get_object()
        self.check_object_permissions(request, subtask)
        serializer = SubTaskSerializer(subtask, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def delete_subtask(self, request, pk=None):
        subtask = self.get_object()
        self.check_object_permissions(request, subtask)
        subtask.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)