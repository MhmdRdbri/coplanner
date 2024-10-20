from django.contrib import admin
from .models import *
from django_celery_beat.models import PeriodicTask, IntervalSchedule

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_name','manager_full_name','end_date', 'status', 'responsible_person', 'domain')
    list_filter = ('status', 'end_date', 'responsible_person','team_members')
    search_fields = ('project_name', 'description', 'domain','team_members')
    date_hierarchy = 'end_date'
    ordering = ('-end_date',)

    fieldsets = (
        (None, {'fields': ('project_name', 'manager_full_name', 'description', 'phone_number', 'team_members' )}),
        ('Project Dates', {'fields': ('start_date', 'end_date', 'domain_end_date','host_end_date')}),
        ('Project Status', {'fields': ('status',)}),
        ('User Permissions', {'fields': ('responsible_person',)}),
        ('Additional Info', {'fields': ('domain', 'design_files', 'contract_files', )}),
    )
    

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

@admin.register(ContentProject)
class ContentProjectAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'project_status', 'start_date', 'end_date', 'photo_frequency', 'videos_per_month')
    list_filter = ('project_status', 'start_date', 'end_date', 'team_members')
    search_fields = ('full_name', 'organization_colors', 'team_members__username', 'damage')
    date_hierarchy = 'end_date'
    ordering = ('-end_date',)

    fieldsets = (
        (None, {'fields': ('full_name', 'contact_number', 'team_members')}),
        ('Project Information', {'fields': ('start_date', 'end_date', 'project_status', 'photo_frequency', 'videos_per_month', 'photos_per_month')}),
        ('Details', {'fields': ('organization_colors', 'collaboration_duration', 'contract_file', 'damage')}),
        ('Additional Services', {'fields': ('consultation', 'caption_writing', 'cover_design', 'post_scenario_writing', 'teaser', 'drone_shot', 'outside_shoot', 'out_of_city_shoot')}),
    )