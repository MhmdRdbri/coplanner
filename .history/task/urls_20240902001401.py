from django.urls import path
from .views import CreateTicketAPIView, ChatRoomListAPIView, SendMessageAPIView, CloseTicketAPIView, TicketListAPIView

app_name = 'task'

urlpatterns = [
    # مسیر برای ایجاد تیکت جدید
    path('tickets/create/', CreateTicketAPIView.as_view(), name='create-ticket'),
    
    # مسیر برای لیست کردن چت‌روم‌ها
    path('chatrooms/', ChatRoomListAPIView.as_view(), name='chatroom-list'),
    
    # مسیر برای ارسال پیام در چت‌روم
    path('chatrooms/<int:chatroom_id>/send/', SendMessageAPIView.as_view(), name='send-message'),
    
    # مسیر برای بستن تیکت و غیرفعال کردن چت‌روم
    path('tickets/<int:ticket_id>/close/', CloseTicketAPIView.as_view(), name='close-ticket'),
    
    # مسیر برای مشاهده تیکت‌ها
    path('tickets/', TicketListAPIView.as_view(), name='ticket-list'),
]
