from .models import *
from rest_framework import serializers
from django.db.models import Q
class FriendRequestSerializer(serializers.ModelSerializer):
    """
    Serializer for creating friend request
    """
    class Meta:
        model = FriendRequest
        fields = ['request_to']

    def create(self, validated_data):
        request_from = self.context.get('request_from')
        request_to  =  validated_data.get('request_to')
        # Check if user has already send the request
        frnd_obj = FriendRequest.objects.filter(Q(request_from = request_from) & Q(request_to = request_to)& Q(status='accepted')| Q(status='pending'))
        if not frnd_obj.exists():
            return  FriendRequest.objects.create(request_from = request_from, request_to = request_to)
        return frnd_obj.last()
    
class FriendRequestUpdateSerializer(serializers.ModelSerializer):
    """ 
    Serializer for accepting and rejecting friend request 
    """
    STATUS_CHOICES = [
        ('accepted', 'accepted'),
        ('rejected', 'rejected'),
    ]

    status = serializers.ChoiceField(choices=STATUS_CHOICES)
    id = serializers.PrimaryKeyRelatedField(queryset=FriendRequest.objects.all())
    class Meta:
        model = FriendRequest
        fields = ['status','id']

    def create(self, validated_data):
        status = validated_data.get('status')
        frnd_req_obj = validated_data.get('id')
        frnd_req_obj.status = status
        frnd_req_obj.save()
        if status == 'accepted':
            frnd_req_obj.request_to.friends.add(frnd_req_obj.request_from)
        return frnd_req_obj
