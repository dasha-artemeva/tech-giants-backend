from django.conf import settings
from django.http import HttpResponseRedirect
from rest_framework import mixins

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.utils.encoders import JSONEncoder
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from applications.jwtauth.api.serializers import (
    LoginUserSerializer,
    RegisterUserSerializer,
    UpdateUserSerializer,
)
from applications.jwtauth.services import login_user
from applications.members.api.serializers import (
    RetrieveUserSerializer,
)
from applications.members.models import User
from applications.members.services import create_user, update_user

AUTH_TAGS = ["Авторизация"]


def authorize_response(
    user: User, token: AccessToken, status_code=status.HTTP_200_OK
) -> Response:
    response = Response(
        data=RetrieveUserSerializer(user).data,
        status=status_code,
    )
    response.set_cookie(
        key=settings.SIMPLE_JWT["AUTH_COOKIE"],
        value=token,
        max_age=60 * 60 * 24 * 7,
    )
    return response


@extend_schema(
    request=RegisterUserSerializer,
    responses={
        status.HTTP_201_CREATED: RetrieveUserSerializer,
    },
    tags=AUTH_TAGS,
)
@api_view(["POST"])
@permission_classes([])
def register(request: Request) -> Response:
    """
    Создание нового пользователя
    """
    serializer = RegisterUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    create_user(**serializer.validated_data)
    user, token = login_user(**serializer.validated_data)
    return authorize_response(user, token, status_code=status.HTTP_201_CREATED)


@extend_schema(
    request=LoginUserSerializer,
    responses={
        status.HTTP_200_OK: RetrieveUserSerializer,
    },
    tags=AUTH_TAGS,
)
@api_view(["POST"])
@permission_classes([])
def login(request: Request) -> Response:
    """
    Войти в аккаунт с использованием email и пароля
    """
    serializer = LoginUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user, token = login_user(**serializer.validated_data)
    return authorize_response(user, token, status_code=status.HTTP_200_OK)


@api_view(["GET", "POST"])
@permission_classes([])
def logout(request: Request):
    response = Response(status=status.HTTP_204_NO_CONTENT)
    response.delete_cookie(settings.SIMPLE_JWT["AUTH_COOKIE"])
    return response


class UserView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=None,
        responses={
            status.HTTP_200_OK: RetrieveUserSerializer,
        },
        tags=AUTH_TAGS,
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        """
        Получить текущего пользователя
        """
        return Response(
            data=RetrieveUserSerializer(request.user).data,
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        request=UpdateUserSerializer,
        responses={
            status.HTTP_200_OK: RetrieveUserSerializer,
        },
        tags=AUTH_TAGS,
    )
    def patch(self, request: Request, *args, **kwargs) -> Response:
        """
        Обновить данные текущего пользователя
        """
        serializer = UpdateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = update_user(
            request.user,
            **serializer.validated_data,
        )
        return Response(
            data=RetrieveUserSerializer(user).data,
            status=status.HTTP_200_OK,
        )
