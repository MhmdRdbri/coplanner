from rest_framework import serializers
from .models import WorkReport

class WorkReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkReport
        fields = ['id', 'user', 'date,', 'content', 'is_approved']
        read_only_fields = ['user', 'date', 'is_approved']