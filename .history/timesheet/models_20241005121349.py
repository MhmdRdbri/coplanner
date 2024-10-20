from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

class Timesheet(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    total_worked_time = models.DurationField(default=timezone.timedelta)

    def __str__(self):
        return f"{self.user} - {self.date}"


     
    @classmethod
    def get_weekly_worked_time(cls, user):
        today = timezone.now().date()
        start_of_week = today - timedelta(days=today.weekday() + 1)
        end_of_week = start_of_week + timedelta(days=5)

        timesheets = cls.objects.filter(user=user, date__range=[start_of_week, end_of_week])
        total_worked_time = sum([timesheet.total_worked_time for timesheet in timesheets], timedelta())
        return total_worked_time

class Pause(models.Model):
    timesheet = models.ForeignKey(Timesheet, on_delete=models.CASCADE, related_name='pauses')
    pause_time = models.DateTimeField()
    resume_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Pause: {self.pause_time} - Resume: {self.resume_time}"
