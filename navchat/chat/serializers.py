from rest_framework import serializers
from .models import ChatRoom

class ChatRoomSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(
        many = True,
        read_only = True
    )
    class Meta:
        model = ChatRoom
        fields = ['id', 'participants', 'created_at']