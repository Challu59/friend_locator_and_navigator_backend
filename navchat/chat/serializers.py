from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import ChatRoom, Message

User = get_user_model()


class UserSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class LastMessageSerializer(serializers.Serializer):
    content = serializers.CharField()
    timestamp = serializers.DateTimeField()
    sender_id = serializers.IntegerField()


class ConversationSerializer(serializers.Serializer):
    room_id = serializers.IntegerField()
    other_user = UserSummarySerializer()
    last_message = LastMessageSerializer(allow_null=True)
    unread_count = serializers.IntegerField()


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