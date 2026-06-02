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
    

class Friendship(models.Model):
    user1 = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name= 'friendships_one',
        on_delete=models.CASCADE
    )
    user2 = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name= 'friendships_two',
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ('user1', 'user2')

    def __str__(self):
        return f'(self.user1) friend with (self.user2)'