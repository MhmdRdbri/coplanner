from django.contrib.auth.models import User
from django.db import models

class Ticket(models.Model):
    STATUS_CHOICES = [
        ('sent', 'Sent'),
        ('in_process', 'In Process'),
        ('answered', 'Answered'),
        ('closed', 'Closed'),
    ]

    title = models.CharField(max_length=255)
    sender = models.ForeignKey(User, related_name='sent_tickets', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_tickets', on_delete=models.CASCADE)
    description = models.TextField()
    file = models.FileField(upload_to='tickets/', blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='sent')

    def __str__(self):
        return f'{self.title} - {self.status}'

class ChatRoom(models.Model):
    ticket = models.OneToOneField(Ticket, related_name='chatroom', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'ChatRoom for Ticket: {self.ticket.title}'

class Message(models.Model):
    chatroom = models.ForeignKey(ChatRoom, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    content = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.sender.username} at {self.date_sent}'
