from django.urls import include, path
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from .views import *


router = DefaultRouter()
router.register('friendrequest', FriendRequestViewSet)

urlpatterns = [
    path('friend_list/', ListFriends.as_view()),
    path('', include(router.urls)),
    path('status/<int:pk>/', UpdateFriendRequestStatus.as_view()),
]