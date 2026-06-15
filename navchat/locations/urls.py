from django.urls import path

from .views import UpdateLocationView, StopSharingView, FriendsLocationView

urlpatterns = [
    path('update/', UpdateLocationView.as_view(), name='update-location'),
    path('stop-sharing/', StopSharingView.as_view(), name='stop-sharing'),
    path('friends/', FriendsLocationView.as_view(), name='friends-locations'),
]
