from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet
from .serializers import * 
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from accounts.serializers import *
from rest_framework import generics
from .throtling import FriendRequestThrottleRate
from rest_framework.views import APIView
# Create your views here.

class FriendRequestViewSet(ModelViewSet):
    """
    GET : list out all the pending request
    POST : send friend request 
    """
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]
    # throttle_classes = [FriendRequestRateThrottle]
    pagination_class = PageNumberPagination
    http_method_names = ['post', 'get']
    
    def get_queryset(self):
        return self.queryset.filter(request_to=self.request.user, status='pending')
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request_from'] = self.request.user
        return context


class ListFriends(generics.ListAPIView):
    """
    View for listing all friends of User.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    
    def get_queryset(self):
        return self.request.user.friends.all()
    

class UpdateFriendRequestStatus(APIView):
    """
    View for handling friendrequest accept or reject status
    """
    serializer_class = FriendRequestUpdateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        status = request.data.get('status')
        serializer = self.serializer_class(data={'id': pk, 'status': status})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data={"message": f"Friend request {status}"})