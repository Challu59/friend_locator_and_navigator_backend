from django.urls import path
from .views import CreateOrGetChatRoomView, MessageListCreateView

urlpatterns = [
    path('rooms/', CreateOrGetChatRoomView.as_view()),
    path('rooms/<int:room_id>/messages', MessageListCreateView.as_view()),
]
