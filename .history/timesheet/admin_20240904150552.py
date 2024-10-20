from django.contrib import admin
from .models import TimeSheet

class TimeSheetAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'start_time', 'end_time', 'total_time']

admin.site.register(TimeSheet, TimeSheetAdmin)
