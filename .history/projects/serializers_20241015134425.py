from rest_framework import serializers
from .models import Project
from account.models import CustomUser

class ProjectSerializer(serializers.ModelSerializer):
    team_members = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), many=True)

    class Meta:
        model = Project
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    team_members = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), many=True)

    class Meta:
        model = ContentProject
        fields = '__all__'