from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# فرض کنید مدل‌های مختلف از اپلیکیشن‌های مختلف ایمپورت می‌شوند
from tickets.models import Ticket
from tasks.models import Task
from chat.models import ChatRoom

class DashboardDataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user

        # چک کردن اینکه آیا کاربر دسترسی ویژه دارد یا خیر
        if user.has_special_access:
            # داده‌هایی که برای کاربر با دسترسی ویژه نمایش داده می‌شود
            tickets_count = Ticket.objects.all().count()
            tasks_count = Task.objects.all().count()
            chatrooms_count = ChatRoom.objects.all().count()
            special_data = {
                'total_users': User.objects.count(),  # مثلا تعداد کل کاربران
                'admin_notes': "This is a special note only for admins",  # اطلاعات خاص دیگر
            }
            data = {
                'tickets_count': tickets_count,
                'tasks_count': tasks_count,
                'chatrooms_count': chatrooms_count,
                'special_data': special_data,
            }
        else:
            # داده‌هایی که برای کاربران عادی نمایش داده می‌شود
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
