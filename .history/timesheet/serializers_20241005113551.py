from rest_framework import serializers
from .models import Timesheet, Pause

class PauseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pause
        fields = ['pause_time', 'resume_time']

class TimesheetSerializer(serializers.ModelSerializer):
    pauses = PauseSerializer(many=True, read_only=True)
    start_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    end_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Timesheet
        fields = ['user', 'date', 'start_time', 'end_time', 'total_worked_time', 'pauses']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        # Format date as 'YYYY-MM-DD'
        representation['date'] = instance.date.strftime('%Y-%m-%d')
        
        # Convert datetime to local time and format
        if isinstance(instance.start_time, datetime):
            start_time_local = timezone.localtime(instance.start_time)
            representation['start_time'] = start_time_local.strftime('%Y-%m-%d %H:%M:%S')
        
        if isinstance(instance.end_time, datetime):
            end_time_local = timezone.localtime(instance.end_time)
            representation['end_time'] = end_time_local.strftime('%Y-%m-%d %H:%M:%S')
        
        return representation