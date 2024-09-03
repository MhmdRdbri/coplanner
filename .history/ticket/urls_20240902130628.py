from django.urls import path
from .views import CreateTicketAPIView, ChatRoomListAPIView, SendMessageAPIView, CloseTicketAPIView, TicketListAPIView

app_name = 'ticket'

urlpatterns = [
    path('tickets/create/', CreateTicketAPIView.as_view(), name='create-ticket'),
    path('chatrooms/', ChatRoomListAPIView.as_view(), name='chatroom-list'),
    path('chatrooms/<int:chatroom_id>/send/', SendMessageAPIView.as_view(), name='send-message'),
    path('tickets/<int:ticket_id>/close/', CloseTicketAPIView.as_view(), name='close-ticket'),
    path('tickets/', TicketListAPIView.as_view(), name='ticket-list'),
]
