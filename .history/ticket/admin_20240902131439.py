from django.contrib import admin
from .models import Ticket, ChatRoom, Message

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'sender', 'receiver', 'date_created', 'status')
    list_filter = ('status', 'date_created')
    search_fields = ('title', 'description', 'sender__username', 'receiver__username')

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('ticket__title', 'ticket__sender__username', 'ticket__receiver__username')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('chatroom', 'sender', 'content', 'date_sent')
    list_filter = ('date_sent',)
    search_fields = ('chatroom__ticket__title', 'sender__username', 'content')
