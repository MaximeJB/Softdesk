from django.contrib.auth import get_user_model
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin,UpdateModelMixin,ListModelMixin
from rest_framework.viewsets import GenericViewSet
from accounts.serializers import UserCreateSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsSelf

User = get_user_model()


class UserViewSet(CreateModelMixin,
                   RetrieveModelMixin,
                   UpdateModelMixin,
                   ListModelMixin,
                   GenericViewSet):
    """
    API endpoint that allows users to be viewed or edited.

    "create" use UserCreateSerializer
    other actions use UserSerializer
    """
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsSelf]

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        return UserSerializer
