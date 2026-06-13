from django.urls import path
from .views import (
    SendFriendRequestView,
    AcceptFriendRequestView,
    RejectFriendRequestView,
    PendingRequestsView,
    FriendsListView,
    SearchUsersView,
)

urlpatterns = [
    path(
        'send/',
        SendFriendRequestView.as_view(),
        name='send-friend-request'
    ),
    path('<int:request_id>/accept/', AcceptFriendRequestView.as_view(), name='accept-friend-request'),
    path('<int:request_id>/reject/', RejectFriendRequestView.as_view(), name='reject-friend-request'),
    path('pending/', PendingRequestsView.as_view(), name = 'pending-requests'),
    path('search/', SearchUsersView.as_view(), name='search-users'),
    path('', FriendsListView.as_view(), name='friends-list'),
]
