from django.db import models
from django.conf import settings

class Ticket(models.Model):
    STATUS_CHOICES = [
        ('sent', 'Sent'),
        ('in_process', 'In Process'),
        ('answered', 'Answered'),
        ('closed', 'Closed')
    ]

    title = models.CharField(max_length=255)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_tickets', on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_tickets', on_delete=models.CASCADE)
    description = models.TextField()
    file = models.FileField(upload_to='tickets/files/', blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='sent')

    def __str__(self):
        return f"Ticket: {self.title} from {self.sender} to {self.receiver}"

class ChatRoom(models.Model):
    ticket = models.OneToOneField(Ticket, related_name='chatroom', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"ChatRoom for {self.ticket}"

class Message(models.Model):
    chatroom = models.ForeignKey(ChatRoom, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='messages', on_delete=models.CASCADE)
    text = models.TextField()
    file = models.FileField(upload_to='messages/files/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender} in {self.chatroom}"