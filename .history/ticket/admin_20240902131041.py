# from django.contrib import admin
# from .models import Ticket, Attachment, Response

# @admin.register(Ticket)
# class TicketAdmin(admin.ModelAdmin):
#     list_display = ['id', 'user', 'subject', 'status', 'created_at', 'updated_at']
#     list_filter = ['status', 'user', 'created_at']
#     search_fields = ['subject', 'message']

# @admin.register(Attachment)
# class AttachmentAdmin(admin.ModelAdmin):
#     list_display = ['id', 'ticket', 'file', 'uploaded_at']
#     list_filter = ['uploaded_at']
#     search_fields = ['ticket__subject']

# @admin.register(Response)
# class ResponseAdmin(admin.ModelAdmin):
#     list_display = ['id', 'ticket', 'user', 'message', 'created_at']
#     list_filter = ['created_at']
#     search_fields = ['ticket__subject', 'message']