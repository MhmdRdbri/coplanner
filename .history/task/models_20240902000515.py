from django.db import models
from django.contrib.auth.models import User

class ChatRoom(models.Model):
    participants = models.ManyToManyField(User)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

class Ticket(models.Model):
    STATUS_CHOICES = [
        ('sent', 'Sent'),
        ('in_process', 'In Process'),
        ('answered', 'Answered'),
        ('closed', 'Closed'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_tickets')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_tickets')
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='sent')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def update_status(self, user):
        if self.status == 'sent' and user == self.receiver:
            self.status = 'in_process'
        elif self.status == 'in_process' and user == self.sender:
            self.status = 'answered'
        self.save()

class ChatMessage(models.Model):
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)