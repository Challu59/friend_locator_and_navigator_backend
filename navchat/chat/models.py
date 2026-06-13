from django.db import models
from django.conf import settings
from django.utils import timezone


class ChatRoom(models.Model):
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='chat_rooms'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        participant_names = ', '.join(self.participants.values_list('username', flat=True))
        return f"Chatroom({participant_names})"
    
class Message(models.Model):
    room = models.ForeignKey(
        ChatRoom,
        on_delete= models.CASCADE,
        related_name='messages'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete= models.CASCADE,
        related_name='sent_messages'
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.sender.username}: {self.content[:30]}"


class RoomReadState(models.Model):
    room = models.ForeignKey(
        ChatRoom,
        on_delete=models.CASCADE,
        related_name='read_states',
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='room_read_states',
    )
    last_read_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('room', 'user')

    def __str__(self):
        return f"{self.user.username} read {self.room_id} at {self.last_read_at}"