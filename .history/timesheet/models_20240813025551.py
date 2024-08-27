# timesheet/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class TimeEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    time_worked = models.DurationField()  # stores time in HH:MM:SS format

    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.time_worked}"