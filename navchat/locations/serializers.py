from rest_framework import serializers

from .models import UserLocation


class UserLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLocation
        fields = ['latitude', 'longitude', 'is_sharing', 'updated_at']
        read_only_fields = ['updated_at']


class FriendLocationSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    updated_at = serializers.DateTimeField()
