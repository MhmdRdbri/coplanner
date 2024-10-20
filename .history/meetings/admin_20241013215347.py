from django.contrib import admin
from .models import Meeting

@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ['title', 'meeting_date', 'description']
    search_fields = ['title', 'description']
    filter_horizontal = ['participants']