from django.contrib.auth    import get_user_model
from rest_framework         import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
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
    password = serializers.CharField(write_only=True, required=True)
    age = serializers.IntegerField(write_only=True, required=True)
    can_be_contacted = serializers.BooleanField(required=True)
    can_data_be_shared = serializers.BooleanField(required=True)

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
        if value < 15:
            raise serializers.ValidationError(
                "Un utilisateur doit avoir au moins 15 ans."
            )
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
