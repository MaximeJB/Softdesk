from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for transforming into json model's infos

    attributes:
        can_be_contacted (BooleanField): Required field for contact permission.
        can_data_be_shared (BooleanField): Required field for data sharing permission.
    """
    can_be_contacted = serializers.BooleanField(required=True)
    can_data_be_shared = serializers.BooleanField(required=True)

    class Meta:
        model = User
        fields = [
            "url",
            "username",
            "email",
            "age",
            "can_be_contacted",
            "can_data_be_shared",
        ]


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new user

    -Age must be at least 15, can't be 13 or under

    Attributes :
        write only password fiel
        age (integer)
        can_be_contacted (BooleanField): contact permission
        can_data_be_shared (BooleanField): Data sharing permission
    """
    password = serializers.CharField(write_only=True, required=True)
    age = serializers.IntegerField(write_only=True, required=True)
    can_be_contacted = serializers.BooleanField()
    can_data_be_shared = serializers.BooleanField()

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "age",
            "can_be_contacted",
            "can_data_be_shared",
        ]

    def validate_age(self, value):
        """
        Ensure that user is at least 15 years old
        """
        if value < 15:
            raise serializers.ValidationError(
                "Un utilisateur doit avoir au moins 15 ans."
            )
        return value

    def create(self, validated_data):
        """
        Create and save a new user with encrypted password
        """
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
