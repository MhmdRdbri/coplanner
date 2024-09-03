from django.db import models
from django.utils import timezone
from account.models import CustomUser

class WorkReport(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    content = models.TextField()

    class Meta:
        unique_together = ('user', 'date')

    def __str__(self):
        return f'{self.user} - {self.date}'