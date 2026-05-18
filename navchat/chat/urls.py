from django.urls import path
from .views import CreateOrGetChatRoomView

urlpatterns = [
    path('rooms/', CreateOrGetChatRoomView.as_view()),
]
