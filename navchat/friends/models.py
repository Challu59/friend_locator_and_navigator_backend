from django.db import models
from django.conf import settings


class FriendRequest(models.Model):
    STATUS_CHOICES= [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='sent_friend_requests',
        on_delete=models.CASCADE
    )

    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name= 'received_friend_requests',
        on_delete=models.CASCADE
    )

    status = models.CharField(
        choices= STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ('sender', 'receiver')

    def __str__(self):
        return f'{self.sender} -> {self.receiver}'