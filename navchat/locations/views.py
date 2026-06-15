from django.contrib.auth import get_user_model
from django.db import models
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from friends.models import Friendship
from .models import UserLocation
from .serializers import UserLocationSerializer

User = get_user_model()


class UpdateLocationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')
        is_sharing = request.data.get('is_sharing', True)

        if latitude is None or longitude is None:
            return Response(
                {'detail': 'latitude and longitude are required'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        location, _ = UserLocation.objects.update_or_create(
            user=request.user,
            defaults={
                'latitude': latitude,
                'longitude': longitude,
                'is_sharing': bool(is_sharing),
            },
        )

        serializer = UserLocationSerializer(location)
        return Response(serializer.data)


class StopSharingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            location = UserLocation.objects.get(user=request.user)
        except UserLocation.DoesNotExist:
            return Response({'detail': 'No location stored'})

        location.is_sharing = False
        location.save(update_fields=['is_sharing', 'updated_at'])
        return Response({'detail': 'Location sharing disabled'})


class FriendsLocationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        friendships = Friendship.objects.filter(
            models.Q(user1=request.user) |
            models.Q(user2=request.user)
        )

        friend_ids = []
        for friendship in friendships:
            if friendship.user1_id == request.user.id:
                friend_ids.append(friendship.user2_id)
            else:
                friend_ids.append(friendship.user1_id)

        friend_locations = UserLocation.objects.filter(
            user_id__in=friend_ids,
            is_sharing=True,
        ).select_related('user')

        data = [
            {
                'id': location.user.id,
                'username': location.user.username,
                'latitude': location.latitude,
                'longitude': location.longitude,
                'updated_at': location.updated_at,
            }
            for location in friend_locations
        ]

        return Response(data)
