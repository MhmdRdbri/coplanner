from rest_framework import serializers
from .models import Project

class ProjectSerializer(serializers.ModelSerializer):
    team_members = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), many=True)

    class Meta:
        model = Project
        fields = '__all__'