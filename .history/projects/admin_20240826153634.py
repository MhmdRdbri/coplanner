from django.contrib import admin
from .models import *
from django_celery_beat.models import PeriodicTask, IntervalSchedule

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'full_name','end_date', 'status', 'priority', 'responsible_person', 'domain', 'team')
    list_filter = ('status', 'priority', 'end_date', 'responsible_person','full_name')
    search_fields = ('name', 'description', 'domain', 'full_name')
    date_hierarchy = 'end_date'
    ordering = ('-end_date',)

    fieldsets = (
        (None, {'fields': ('name', 'description', 'full_name', 'phone_number' )}),
        ('Project Dates', {'fields': ('start_date', 'end_date', 'domain_start_date', 'domain_end_date', 'host_start_date', 'host_end_date')}),
        ('Project Status', {'fields': ('status', 'priority')}),
        ('User Permissions', {'fields': ('responsible_person', 'design_team_members', 'deploy_team_members')}),
        ('Additional Info', {'fields': ('domain', 'design_files', 'team')}),
    )
    filter_horizontal = ('design_team_members', 'deploy_team_members')
    

# # Create the schedule
# schedule, created = IntervalSchedule.objects.get_or_create(
#     every=1,
#     period=IntervalSchedule.DAYS,
# )

# # Create the periodic task
# PeriodicTask.objects.create(
#     interval=schedule,
#     name='Check project end dates',
#     task='project.tasks.check_project_end_dates',  # Use the path to your task
# )

admin.site.register(SMSLog)