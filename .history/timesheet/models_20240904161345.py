from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class TimeSheet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='timesheets')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    paused_time = models.DurationField(default=timezone.timedelta)
    date = models.DateField(auto_now_add=True)

    def total_time(self):
        if self.end_time:
            total = self.end_time - self.start_time - self.paused_time
            return total if total > timezone.timedelta() else timezone.timedelta()
        return None

    def __str__(self):
        return f"{self.user.last_name} - {self.date}"
