from rest_framework import serializers

from applications.members.enums import ParticipationRequestState
from applications.members.models import User


class RetrieveUserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    middle_name = serializers.CharField()
    name = serializers.CharField()
    phone_number = serializers.CharField()
    birth_date = serializers.DateField()

    is_filled_by_user = serializers.BooleanField()


class RetrieveShortUserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    name = serializers.CharField()


class RetrieveParticipationRequestSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    authors = serializers.CharField()
    text = serializers.CharField()
    media = serializers.FileField()
    state = serializers.ChoiceField(choices=ParticipationRequestState.choices)
    user = RetrieveUserSerializer(read_only=True)
    assigned_to = RetrieveShortUserSerializer(read_only=True)
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


class CreateParticipationRequestSerializer(serializers.Serializer):
    title = serializers.CharField()
    authors = serializers.CharField()
    text = serializers.CharField()
    media = serializers.FileField()


class UpdateParticipationRequestSerializer(serializers.Serializer):
    assigned_to = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False,
    )
    state = serializers.ChoiceField(
        choices=ParticipationRequestState.choices,
        required=False,
    )
