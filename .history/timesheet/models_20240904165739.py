from django.db import models
from django.conf import settings
from django.utils import timezone

class Timesheet(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    total_worked_time = models.DurationField(default=timezone.timedelta)

    def __str__(self):
        return f"{self.user} - {self.date}"

class Pause(models.Model):
    timesheet = models.ForeignKey(Timesheet, on_delete=models.CASCADE, related_name='pauses')
    pause_time = models.DateTimeField()
    resume_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Pause: {self.pause_time} - Resume: {self.resume_time}"
