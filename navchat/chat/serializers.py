from rest_framework import serializers
from .models import ChatRoom, Message

class ChatRoomSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(
        many = True,
        read_only = True
    )
    class Meta:
        model = ChatRoom
        fields = ['id', 'participants', 'created_at']

class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(
        source = 'sender.username',
        read_only = True
    )
    class Meta:
        model = Message
        fields = ['id', 'room', 'sender', 'sender_username', 'content', 'timestamp']
        read_only_fields = ['id', 'room', 'sender', 'sender_username', 'timestamp']