from django.db import models
from django.conf import settings
from django.utils import timezone

class Task(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    due_date = models.DateField()
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def update_is_done(self):
        if self.subtasks.filter(is_done=False).exists():
            self.is_done = False
        else:
            self.is_done = True
        self.save()