from rest_framework import serializers

from applications.members.api.serializers import RetrieveUserSerializer
from applications.members.models import User


class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField()

    def validate(self, attrs):
        if any(key not in attrs for key in ["username", "email"]):
            raise serializers.ValidationError(
                'Введите поле "username" или "email"'
            )
        return attrs



class TokenSerializer(serializers.Serializer):
    token = serializers.CharField()
    user = RetrieveUserSerializer(read_only=True)


class RegisterUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8)


class UpdateUserSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    middle_name = serializers.CharField()
    phone_number = serializers.CharField()
    birth_date = serializers.DateField()
