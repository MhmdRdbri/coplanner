from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from .serializers import *
from .models import *
from django.urls import reverse
from django.conf import settings
from .serializers import *
import http.client
import json
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrReadOnly
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
import logging
import asyncio
from telegram import Bot


class CustomUserLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = CustomUserLoginSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            user = CustomUser.objects.get(phone_number=phone_number)

            refresh = RefreshToken.for_user(user)
            access = AccessToken.for_user(user)

            # Determine the role based on user's attributes
            if user.is_active and user.is_staff and user.has_special_access:
                role = 'manager'
            elif user.is_active:
                role = 'employee'
            else:
                role = 'guest'  # Default role if no conditions match

            # Add the role to the access token's payload
            access['role'] = role

            return Response({
                'access': str(access),
                'refresh': str(refresh),
                'role': role,  # Optionally, include the role in the response as a separate field
            }, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetInitiateAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            new_password = serializer.validated_data['new_password']
            token = PasswordResetToken.create_code(user)
            try:
                user = CustomUser.objects.get(phone_number=phone_number)
                token = PasswordResetToken.create_code(user)
                
                chat_id = user.telegram_chat_id
                bot_token = '7052281105:AAG5x1yux4ryfDzvfAmn1mwuVqa4LmBtKkk'
                bot = Bot(token=bot_token)
                message = f"کد یکبار مصرف شما برای تغییر رمز '{token.token}' است"
                
                logging.debug(f"Attempting to send message to chat_id: {chat_id}")

                asyncio.run(bot.send_message(chat_id=chat_id, text=message))
                logging.info(f"Sent message to {chat_id}: {message}")

                return Response({'message': 'Verification code sent successfully'}, status=status.HTTP_200_OK)

            except CustomUser.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

            

            print(token.token)

            conn = http.client.HTTPSConnection("api2.ippanel.com")
            payload = json.dumps({
            "code": "se2e1hipxk5amv4",
            "sender": "+983000505",
            "recipient": phone_number,
            "variable": {
                "verification-code": token.token,
            }
            })
            headers = {
            'apikey': ' SZtX_MYwI2E0jWqdkrSoDV3-02u0yF-l2c1LXgZVZpw= ',
            'Content-Type': 'application/json'
            }
            conn.request("POST", "/api/v1/sms/pattern/normal/send", payload, headers)
            res = conn.getresponse()
            data = res.read()
            print(data.decode("utf-8"))
            
            
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class PasswordResetVerifyAPIView(APIView):

    serializer_class = PasswordResetSerializer

    def post(self, request, token, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            new_password = serializer.validated_data['new_password']

            token_obj = PasswordResetToken.objects.filter(token=token).first()
            if not token_obj:
                return Response({'error': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)

            user = token_obj.user
            user.set_password(new_password)
            user.save()

            token_obj.delete()
            PasswordResetToken.delete_code(token_obj)

            return Response({'message': 'Password reset successful'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = PendingRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Registration request submitted for approval.'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            access_token = request.headers.get("Authorization").split()[1]
            
            if refresh_token is None:
                return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
            if access_token is None:
                return Response({"error": "Access token is required"}, status=status.HTTP_400_BAD_REQUEST)

            # Blacklist the refresh token
            refresh_token_obj = RefreshToken(refresh_token)
            refresh_token_obj.blacklist()
            
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)