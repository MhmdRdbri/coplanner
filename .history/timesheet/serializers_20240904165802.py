from rest_framework import serializers
from .models import Timesheet, Pause

class PauseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pause
        fields = ['pause_time', 'resume_time']

class TimesheetSerializer(serializers.ModelSerializer):
    pauses = PauseSerializer(many=True, read_only=True)

    class Meta:
        model = Timesheet
        fields = ['user', 'date', 'start_time', 'end_time', 'total_worked_time', 'pauses']
