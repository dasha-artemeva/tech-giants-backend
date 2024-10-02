import traceback

from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

from applications.common.exceptions import (
    BaseServiceException,
    PermissionDeniedException,
)


def custom_exception_handler(exc: BaseException, context: dict):
    response = exception_handler(exc, context)

    if isinstance(exc, AssertionError) and isinstance(
        exc.args[0], BaseServiceException
    ):
        exc = exc.args[0].with_traceback(exc.__traceback__)

    if isinstance(exc, PermissionDeniedException):
        response = Response(
            data={"detail": exc.detail},
            status=status.HTTP_403_FORBIDDEN,
        )

    elif isinstance(exc, BaseServiceException):
        response = Response(
            data={"detail": exc.detail},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if settings.DEBUG and isinstance(getattr(response, "data", None), dict):
        response.data.update({"__debug": traceback.format_exception(exc)})

    return response
