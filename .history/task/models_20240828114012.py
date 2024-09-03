from django.db import models
from django.conf import settings
from django.utils import timezone

class Task(models.Model):
    STATUS_CHOICES = [
        ('undone', 'Undone'),
        ('done', 'Done'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateTimeField()
    file = models.FileField(upload_to='task_files/', null=True, blank=True)
    sender = models.ForeignKey(CustomUser, related_name='sent_tasks', on_delete=models.CASCADE)
    receiver = models.ForeignKey(CustomUser, related_name='received_tasks', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='undone')

    def __str__(self):
        return self.title