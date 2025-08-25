from django.shortcuts import render
from rest_framework import viewsets
from accounts.serializers import UserSerializer, UserCreateSerializer
from django.contrib.auth import get_user_model


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by('-date_joined')
    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer
    
    
