from rest_framework import serializers
from account.models import CustomUser, Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


    def update(self, instance, validated_data):
        phone_number = validated_data.get('phone_number', instance.phone_number)
        if phone_number and phone_number != instance.phone_number:
            instance.user.phone_number = phone_number
            instance.user.save()
        return super().update(instance, validated_data)

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = CustomUser
        fields = ['phone_number', 'full_name', 'is_active', 'is_staff', 'profile']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)

        # Update the CustomUser fields
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.is_staff = validated_data.get('is_staff', instance.is_staff)
        instance.save()

        # Update or create the profile
        if profile_data:
            Profile.objects.update_or_create(user=instance, defaults=profile_data)

        return instance