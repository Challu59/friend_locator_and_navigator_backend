from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import FriendRequest
from .serializers import FriendRequestSerializer

class SendFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        receiver_id = request.data.get('receiver_id')

        if request.user.id == receiver_id:
            return Response(
                {'error': 'Cannot send request to yourself'},
                status = status.HTTP_400_BAD_REQUEST
            )
        
        friend_request, created = (
            FriendRequest.objects.get_or_create(
                sender = request.user,
                receiver_id = receiver_id
            )
        )

        serializer = FriendRequestSerializer(friend_request)

        return Response(serializer.data)
        