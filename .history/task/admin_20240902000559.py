from django.contrib import admin
from .models import Task

# class TaskAdmin(admin.ModelAdmin):
#     list_display = ('title', 'sender', 'receiver', 'due_date', 'status',)
#     list_filter = ('status', 'due_date', 'created_at')
#     search_fields = ('title', 'sender__username', 'receiver__username')
#     readonly_fields = ('created_at', 'updated_at')

#     def save_model(self, request, obj, form, change):
#         if not obj.sender_id:
#             obj.sender = request.user
#         super().save_model(request, obj, form, change)

# admin.site.register(Task, TaskAdmin)