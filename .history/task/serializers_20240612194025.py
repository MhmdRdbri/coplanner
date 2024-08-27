# myapp/serializers.py

from rest_framework import serializers
from .models import Task, SubTask

class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = ['id', 'task', 'title', 'is_done']
        read_only_fields = ['id']

class TaskSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer(many=True, read_only=True)
    is_done = serializers.ReadOnlyField()  # Ensure the field is read-only

    class Meta:
        model = Task
        fields = ['id', 'user', 'title', 'due_date', 'is_done', 'subtasks', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']