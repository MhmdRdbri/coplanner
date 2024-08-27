# myapp/admin.py

from django.contrib import admin
from .models import Task

class SubTaskInline(admin.TabularInline):
    model = SubTask
    extra = 1
    fields = ['title', 'is_done']
    readonly_fields = ['is_done']  # Read-only for `is_done` field in inline

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'due_date', 'is_done', 'created_at']
    list_filter = ['due_date', 'user', 'is_done']
    search_fields = ['title', 'user__phone_number']
    inlines = [SubTaskInline]
    actions = ['mark_as_done', 'mark_as_not_done']

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def mark_as_done(self, request, queryset):
        queryset.update(is_done=True)
        for task in queryset:
            task.subtasks.update(is_done=True)
            task.save()
    mark_as_done.short_description = "Mark selected tasks as done"

    def mark_as_not_done(self, request, queryset):
        queryset.update(is_done=False)
        for task in queryset:
            task.subtasks.update(is_done=False)
            task.save()
    mark_as_not_done.short_description = "Mark selected tasks as not done"

@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'task', 'is_done']
    list_filter = ['is_done', 'task__due_date', 'task__user']
    search_fields = ['title', 'task__title', 'task__user__phone_number']
    actions = ['mark_as_done', 'mark_as_not_done']

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def mark_as_done(self, request, queryset):
        queryset.update(is_done=True)
        for subtask in queryset:
            subtask.task.update_is_done()
    mark_as_done.short_description = "Mark selected subtasks as done"

    def mark_as_not_done(self, request, queryset):
        queryset.update(is_done=False)
        for subtask in queryset:
            subtask.task.update_is_done()
    mark_as_not_done.short_description = "Mark selected subtasks as not done"