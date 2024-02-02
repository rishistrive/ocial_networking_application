from django.shortcuts import render

# Create your views here.
from .serializers import MyTokenObtainPairSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import *
from .serializers import *
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import  status
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination

class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class UserSearchViewSet(APIView):
    """
    View Returns  User  searched by name or  Email.
    """
    queryset= CustomUser.objects
    pagination_class = PageNumberPagination
    pagination_class.page_size = 10
    
    def get(self, request):
        user_search = request.GET.get('search')
        search_result =  self.queryset.filter(Q(email__iexact=user_search) | Q (first_name__icontains = user_search) |Q(last_name__icontains = user_search))
        serialized_data = ''
        if search_result:
            serialized_data = UserSerializer(search_result , many = True)
            return Response(serialized_data.data , status=status.HTTP_200_OK)
        return Response({'message':' user not found'}, status= status.HTTP_200_OK)
