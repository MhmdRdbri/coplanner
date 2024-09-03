from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from account.models import *

class DashboardDataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user

        if user.has_special_access:
            users_count = CustomUser.objects.all().count()
            tasks_count = Task.objects.all().count()
            chatrooms_count = ChatRoom.objects.all().count()
            special_data = {
                'total_users': User.objects.count(),
                'admin_notes': "This is a special note only for admins",
            }
            data = {
                'tickets_count': tickets_count,
                'tasks_count': tasks_count,
                'chatrooms_count': chatrooms_count,
                'special_data': special_data,
            }