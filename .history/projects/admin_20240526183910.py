# projects/admin.py
from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'status', 'priority', 'responsible_person')
    list_filter = ('status', 'priority', 'start_date', 'end_date', 'responsible_person')
    search_fields = ('name', 'description')
    date_hierarchy = 'start_date'
    ordering = ('-start_date',)

    fieldsets = (
        (None, {'fields': ('name', 'description')}),
        ('Project Dates', {'fields': ('start_date', 'end_date')}),
        ('Project Status', {'fields': ('status', 'priority')}),
        ('User Permissions', {'fields': ('responsible_person',)}),
    )