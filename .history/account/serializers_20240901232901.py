from rest_framework import serializers
from .models import *
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)

#         # Determine the role based on the user's fields
#         if user.is_active and user.is_staff and user.has_special_access:
#             role = 'manager'
#         elif user.is_active:
#             role = 'employee'
#         else:
#             role = 'guest'  # Default role or additional role logic can go here

#         # Add the role to the token
#         token['role'] = role

#         return token



class CustomUserLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        phone_number = data.get('phone_number')
        password = data.get('password')

        if phone_number and password:
            user = CustomUser.objects.filter(phone_number=phone_number).first()
            if user:
                if user.check_password(password):
                    if user.is_active:
                        return data
                    else:
                        raise serializers.ValidationError("User account is inactive.")
                else:
                    raise serializers.ValidationError("Incorrect password.")
            else:
                raise serializers.ValidationError("User with this phone number does not exist.")
        else:
            raise serializers.ValidationError("Phone number and password are required.")

class PasswordResetSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    new_password = serializers.CharField()


class PendingRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PendingRegistration
        fields = '__all__'

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ('phone_number',)
        read_only_fields = ('user',)