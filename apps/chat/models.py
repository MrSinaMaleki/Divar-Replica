import datetime

from django.db import models
from apps.account.models import User
from apps.post.models import Post

# Create your models here.
class Message(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='messages',
        help_text="Post"
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages',
        help_text="The sender"
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_messages',
        help_text="The REciver"
    )
    content = models.TextField(help_text="The content of the message.")
    timestamp = models.DateTimeField(default=datetime.time, help_text="The time the message was sent.")
    is_read = models.BooleanField(default=False, help_text="read?")

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver} on {self.post.title}"
