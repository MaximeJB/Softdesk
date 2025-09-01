from django.contrib.auth import get_user_model
from rest_framework import viewsets
from accounts.serializers import UserCreateSerializer, UserSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.

    "create" use UserCreateSerializer
    other actions use UserSerializer
    """
    queryset = User.objects.all().order_by("-date_joined")

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        return UserSerializer
