from django.utils import timezone

from .models import Message, RoomReadState


def get_unread_count(room, user):
    read_state = RoomReadState.objects.filter(room=room, user=user).first()
    unread_messages = room.messages.exclude(sender=user)

    if read_state:
        unread_messages = unread_messages.filter(timestamp__gt=read_state.last_read_at)

    return unread_messages.count()


def mark_room_as_read(room, user):
    RoomReadState.objects.update_or_create(
        room=room,
        user=user,
        defaults={'last_read_at': timezone.now()},
    )
