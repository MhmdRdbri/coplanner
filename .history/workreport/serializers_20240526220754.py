# workreport/serializers.py
from rest_framework import serializers
from .models import WorkReport

class WorkReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkReport
        fields = '__all__'
        read_only_fields = ['user', 'date']