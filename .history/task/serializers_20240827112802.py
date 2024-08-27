# myapp/serializers.py

from rest_framework import serializers
from .models import Task
class TaskSerializer(serializers.ModelSerializer):
    is_done = serializers.ReadOnlyField()  # Ensure the field is read-only

    class Meta:
        model = Task
        fields = ['id', 'user', 'title', 'due_date', 'is_done', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']