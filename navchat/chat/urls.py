from django.urls import path
from .views import (
    CreateOrGetChatRoomView,
    MessageListCreateView,
    ConversationListView,
    MarkRoomReadView,
)

urlpatterns = [
    path('conversations/', ConversationListView.as_view()),
    path('rooms/', CreateOrGetChatRoomView.as_view()),
    path('rooms/<int:room_id>/read/', MarkRoomReadView.as_view()),
    path('rooms/<int:room_id>/messages', MessageListCreateView.as_view()),
]
