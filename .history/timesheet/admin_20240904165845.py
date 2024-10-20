from django.contrib import admin
from .models import Timesheet, Pause

@admin.register(Timesheet)
class TimesheetAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'start_time', 'end_time', 'total_worked_time']
    list_filter = ['user', 'date']
    search_fields = ['user__username', 'date']

@admin.register(Pause)
class PauseAdmin(admin.ModelAdmin):
    list_display = ['timesheet', 'pause_time', 'resume_time']
    list_filter = ['timesheet__user', 'pause_time']
    search_fields = ['timesheet__user__username']
