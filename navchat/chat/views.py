from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import ChatRoom, Message
from .serializers import ChatRoomSerializer, MessageSerializer

User = get_user_model()

class CreateOrGetChatRoomView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        # test block start
        print("View is running")
        print("Authenticated user:", request.user)
        print("Request data:", request.data)
        print("ChatRoom model:", ChatRoom)
        print("Serializer model:", ChatRoomSerializer.Meta.model)
        print("Are they same?", ChatRoomSerializer.Meta.model is ChatRoom)
        other_user_id = request.data.get("user_id")
        # test block over

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
        except User.DoesNotExist:
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
        existing_room = (
            ChatRoom.objects.filter(participants = current_user)
            .filter(participants = other_user)
            .distinct()
            .first()
        )

        if existing_room:
            serializer = ChatRoomSerializer(existing_room)

            #test block start
            print("Fields registered:", list(serializer.fields.keys()))
            print("serializer data:", serializer.data)
            #test block over

            return Response(serializer.data)

        # if a ChatRoom does not exist with the requested user, create it
        room = ChatRoom.objects.create()
        room.participants.add(current_user, other_user)

        serializer = ChatRoomSerializer(room)
        return Response(serializer.data, status = status.HTTP_201_CREATED)

        
class MessageListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    # helper function to check if room exists and if the user belongs to the room
    def get_room(self, room_id, user):
        room = get_object_or_404(ChatRoom, id = room_id)
        if not room.participants.filter(id = user.id).exists():
            return None
        return room
    
    # function to return room messages
    def get(self, request, room_id):
        room = self.get_room(room_id, request.user)

        if room is None:
            return Response(
                {'detail': 'Access denied'},
                status=status.HTTP_403_FORBIDDEN,
            )
        messages = room.messages.all()

        serializer = MessageSerializer(messages, many = True)
        return Response(serializer.data)
    

    # function to post new message from the frontenc
    def post(self, request, room_id):
        room = self.get_room(room_id, request.user)

        if room is None:
            return Response(
                {'detail': 'Access denied'},
                status=status.HTTP_403_FORBIDDEN,
            )
        
        serializer = MessageSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(
                room = room,
                sender = request.user
            )

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )





