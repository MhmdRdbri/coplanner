from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TicketViewSet, ChatRoomViewSet, MessageViewSet

app_name = 'ticket'

router = DefaultRouter()
router.register(r'tickets', TicketViewSet, basename='ticket')
router.register(r'chatrooms', ChatRoomViewSet, basename='chatroom')
router.register(r'messages', MessageViewSet, basename='message')


urlpatterns = [
    path('', include(router.urls)),
]
