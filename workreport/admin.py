from django.contrib import admin
from .models import WorkReport

@admin.register(WorkReport)
class WorkReportAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'content')
    list_filter = ('date', 'user')
    search_fields = ('user__phone_number', 'content')