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
        representation['date'] = instance.date.strftime('%Y-%m-%d')  # Ensure 'date' is formatted correctly
        
        # Format start_time and end_time manually if needed
        if isinstance(instance.start_time, datetime):
            representation['start_time'] = instance.start_time.strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(instance.end_time, datetime):
            representation['end_time'] = instance.end_time.strftime('%Y-%m-%d %H:%M:%S')
        
        return representation