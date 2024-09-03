from django.contrib import admin
from .models import Ticket, ChatRoom, Message

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'sender', 'receiver', 'status', 'date')
    list_filter = ('status', 'date')
    search_fields = ('title', 'description', 'sender__username', 'receiver__username')

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'is_active')
    list_filter = ('is_active',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('chatroom', 'sender', 'text', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('text', 'sender__username', 'chatroom__ticket__title')