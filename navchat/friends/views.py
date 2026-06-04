from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import models

from .models import FriendRequest, Friendship
from .serializers import FriendRequestSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

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
        
class AcceptFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, request_id):
        try:
            friend_request = FriendRequest.objects.get(
                id = request_id,
                receiver = request.user,
                status = 'pending'
            )
        except FriendRequest.DoesNotExist:
            return Response(
                {
                    'error': 'Request not found'
                },
                status = status.HTTP_404_NOT_FOUND
            )
        friend_request.status = 'accepted'
        friend_request.save()

        user1 = min(
            friend_request.sender.id,
            friend_request.receiver.id,
        )
        user2 = min(
            friend_request.sender.id,
            friend_request.receiver.id,
        )

        Friendship.objects.get_or_create(
            user1_id = user1,
            user2_id = user2,
        )

        return Response(
            {
                'message': 'Friend request accepted'
            }
        )
    
class RejectFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, request_id):
        try:
            friend_request = FriendRequest.objects.get(
                id = request_id,
                receiver = request.user,
                status = 'pending'
            )
        except FriendRequest.DoesNotExist:
            return Response(
                {
                    'error': 'Request not found'
                },
                status = status.HTTP_404_NOT_FOUND
            )
        friend_request.status = 'rejected'
        friend_request.save()

        return Response(
            {
                'message': 'friend request rejected'
            }
        )
    
class PendingRequestsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        requests = FriendRequest.objects.filter(
            receiver = request.user,
            status = 'pending'
        )
    
        serializer = FriendRequestSerializer(
            requests, many = True
        )

        return Response(serializer.data)

class FriendsListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        friendships = Friendship.objects.filter(
            models.Q(user1 = request.user) |
            models.Q(user2 = request.user)
        )
        
        friends = []

        for friendship in friendships:
            if friendship.user1 == request.user:
                friends.append(friendship.user2)
            else:
                friends.append(friendship.user1)\
        
        data = [
            {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            }
            for user in friends
        ]
        return Response(data)
            