from django.contrib import admin
from .models import Meeting

@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'meeting_date']
    search_fields = ['title', 'description']
    list_filter = ['meeting_date', 'participants']
