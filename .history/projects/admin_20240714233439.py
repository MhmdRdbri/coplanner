from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'full_name', 'start_date', 'end_date', 'status', 'priority', 'responsible_person', 'domain', 'team')
    list_filter = ('status', 'priority', 'start_date', 'end_date', 'responsible_person', 'team')
    search_fields = ('name', 'description', 'domain')
    date_hierarchy = 'start_date'
    ordering = ('-start_date',)

    fieldsets = (
        (None, {'fields': ('name', 'description')}),
        ('Project Dates', {'fields': ('start_date', 'end_date', 'domain_start_date', 'domain_end_date')}),
        ('Project Status', {'fields': ('status', 'priority')}),
        ('User Permissions', {'fields': ('responsible_person', 'design_team_members', 'deploy_team_members')}),
        ('Additional Info', {'fields': ('domain', 'design_files', 'team')}),
    )
    filter_horizontal = ('design_team_members', 'deploy_team_members')