from rest_framework import serializers
from .models import FriendRequest

class FriendRequestSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(
        source = 'sender.username',
        read_only = True
    )

    receiver_username = serializers.CharField(
        source = 'receiver.username',
        read_only = True
    )

    class Meta:
        model = FriendRequest
        fields = '__all__'

