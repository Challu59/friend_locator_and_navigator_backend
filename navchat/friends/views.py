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
        print("REQUEST DATA:", request.data)

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
        user2 = max(
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

class SearchUsersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.query_params.get('q', '').strip()
        users = User.objects.exclude(id=request.user.id)

        if query:
            users = users.filter(
                models.Q(username__icontains=query) |
                models.Q(email__icontains=query)
            )

        friendships = Friendship.objects.filter(
            models.Q(user1=request.user) |
            models.Q(user2=request.user)
        )
        friend_ids = set()
        for friendship in friendships:
            if friendship.user1_id == request.user.id:
                friend_ids.add(friendship.user2_id)
            else:
                friend_ids.add(friendship.user1_id)

        pending_sent = set(
            FriendRequest.objects.filter(
                sender=request.user,
                status='pending',
            ).values_list('receiver_id', flat=True)
        )
        pending_received = set(
            FriendRequest.objects.filter(
                receiver=request.user,
                status='pending',
            ).values_list('sender_id', flat=True)
        )

        results = []
        for user in users[:30]:
            if user.id in friend_ids:
                relationship = 'friend'
            elif user.id in pending_sent:
                relationship = 'pending_sent'
            elif user.id in pending_received:
                relationship = 'pending_received'
            else:
                relationship = 'none'

            results.append({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'relationship': relationship,
            })

        return Response(results)


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
                friends.append(friendship.user1)
        
        data = [
            {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            }
            for user in friends
        ]
        return Response(data)
            