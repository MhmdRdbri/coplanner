from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from tickets.models import Ticket
from tasks.models import Task
from chat.models import ChatRoom
from account.models import *
from workreport.models import *
from Project.models import *

class DashboardDataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user

        if user.has_special_access:
            users_count = CustomUser.objects.all().count()
            workreports_count = Workreport.objects.all().count()
            project_count = Project.objects.filter(project_status=in_progress).count()
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
        else:
            tickets_count = Ticket.objects.filter(sender=user).count()
            tasks_count = Task.objects.filter(receiver=user).count()
            chatrooms_count = ChatRoom.objects.filter(members=user).count()
            data = {
                'tickets_count': tickets_count,
                'tasks_count': tasks_count,
                'chatrooms_count': chatrooms_count,
            }

        # بازگرداندن داده‌ها به عنوان JSON
        return Response(data)
