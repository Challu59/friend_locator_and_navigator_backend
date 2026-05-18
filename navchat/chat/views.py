from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import ChatRoom
from .serializers import ChatRoomSerializer

User = get_user_model

class CreateOrGetChatRoomView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        other_user_id = request.data.get("user_id")

        # if no user_id in request
        if not other_user_id:
            return Response(
                {'detail': "user_id is required"},
                status= status.HTTP_400_BAD_REQUEST,
            )
        
        try:
            #get other user id to chat with
            other_user = User.objects.get(id = other_user_id)

        # if user does not exist
        except User.DoesNotExists:
            return Response(
                {'detail': 'User not found.'},
                status = status.HTTP_404_NOT_FOUND,
            )
        
        # current authenticated user making request
        current_user = request.user

        if current_user.id == other_user.id:
            return Response(
                {'detail': 'Cannot create a chat with yourself.'},
                status= status.HTTP_400_BAD_REQUEST,
            )
        
        # if a ChatRoom already exists with the users, return it
        existing_room = {
            ChatRoom.objects.filter(participants = current_user)
            .filter(participants = other_user)
            .distinct()
            .first()
        }

        if existing_room:
            serializer = ChatRoomSerializer(existing_room)
            return Response(serializer.data)

        # if a ChatRoom does not exist with the requested user, create it
        room = ChatRoom.objects.create()
        room.participants.add(current_user, other_user)

        serializer = ChatRoomSerializer(room)
        return Response(serializer.data, status = status.HTTP_201_CREATED)

        



