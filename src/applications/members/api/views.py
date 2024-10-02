from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from applications.common.permissions import require_permission
from applications.members.api.serializers import (
    RetrieveUserSerializer,
    RetrieveParticipationRequestSerializer,
    CreateParticipationRequestSerializer,
    UpdateParticipationRequestSerializer,
)
from applications.members.models import (
    User,
    ParticipationRequestState,
    ParticipationRequest,
)
from applications.members.services import (
    create_participation_request,
    update_participation_request,
)

USER_TAGS = ["Пользователи"]
PARTICIPATION_REQUEST_TAGS = ["Заявки на участие"]


class UserViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = RetrieveUserSerializer

    @extend_schema(
        responses=RetrieveUserSerializer(many=True),
        tags=USER_TAGS,
    )
    @require_permission("members.view_user")
    def list(self, request: Request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        responses=RetrieveUserSerializer,
        tags=USER_TAGS,
    )
    @require_permission("members.view_user")
    def retrieve(self, request: Request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class ParticipationRequestViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    serializer_class = RetrieveParticipationRequestSerializer
    queryset = ParticipationRequest.objects.all()

    def get_queryset(self):
        if not self.request.user.has_perm(ParticipationRequest.permissions.MODERATOR):
            self.queryset = self.queryset.filter(
                user=self.request.user,
            )
        return super().get_queryset()

    @extend_schema(
        responses={
            status.HTTP_200_OK: RetrieveParticipationRequestSerializer(many=True),
        },
        tags=PARTICIPATION_REQUEST_TAGS,
    )
    @require_permission("members.view_participationrequest")
    def list(self, request: Request, *args, **kwargs):
        """
        Список заявок.
        Если запрашивает модератор будут все заявки
        """
        return super().list(request, *args, **kwargs)

    @extend_schema(
        responses={
            status.HTTP_200_OK: RetrieveParticipationRequestSerializer,
        },
        tags=PARTICIPATION_REQUEST_TAGS,
    )
    @require_permission("members.view_user")
    def retrieve(self, request: Request, *args, **kwargs):
        """
        Просмотр заявки
        """
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        responses={
            status.HTTP_201_CREATED: RetrieveParticipationRequestSerializer,
        },
        tags=PARTICIPATION_REQUEST_TAGS,
    )
    @require_permission("members.create_participationrequest")
    def create(self, request: Request, *args, **kwargs):
        """
        Создание заявки на участие в конференции
        """
        serializer = CreateParticipationRequestSerializer(
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        participation = create_participation_request(
            request.user, **serializer.validated_data
        )
        return Response(
            data=self.get_serializer(participation).data,
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(
        responses={
            status.HTTP_200_OK: RetrieveParticipationRequestSerializer,
        },
        tags=PARTICIPATION_REQUEST_TAGS,
    )
    @require_permission(ParticipationRequest.permissions.MODERATOR)
    def partial_update(self, request: Request, *args, **kwargs):
        """
        Редактирование заявки модератором
        """
        instance = self.get_object()
        serializer = UpdateParticipationRequestSerializer(
            data=request.data,
            context=self.get_serializer_context(),
        )
        serializer.is_valid(raise_exception=True)
        instance = update_participation_request(instance, **serializer.validated_data)
        return Response(
            data=self.get_serializer(instance).data,
            status=status.HTTP_200_OK,
        )
