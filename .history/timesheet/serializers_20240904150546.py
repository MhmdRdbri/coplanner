from rest_framework import serializers
from .models import TimeSheet

class TimeSheetSerializer(serializers.ModelSerializer):
    total_time = serializers.DurationField(read_only=True)

    class Meta:
        model = TimeSheet
        fields = ['id', 'user', 'start_time', 'end_time', 'paused_time', 'date', 'total_time']
        read_only_fields = ['user', 'date', 'total_time']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
