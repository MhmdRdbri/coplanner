from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'due_date', 'file', 'receiver', 'status']
        read_only_fields = ['sender']  # 'sender' is read-only