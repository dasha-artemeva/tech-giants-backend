from django.conf import settings
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response

from applications.api.serializers import ActiveConferenceSerializer
from constance import config

@extend_schema(
    request=None,
    responses={
        status.HTTP_200_OK: ActiveConferenceSerializer,
    },
    tags=['Конференция']
)
@api_view(['GET'])
@permission_classes([])
def active_conference(request: Request) -> Response:
    data = {
        name: getattr(config, f'{settings.ACTIVE_CONFERENCE_CONSTANCE_PREFIX}{name.upper()}')
        for name in ActiveConferenceSerializer().fields.keys()
    }
    return Response(
        data=ActiveConferenceSerializer(data).data,
        status=status.HTTP_200_OK,
    )