import functools

from django.conf import settings
from django.utils.functional import classproperty
from rest_framework.request import Request

from applications.common.exceptions import PermissionDeniedException


class RequirePermission:
    def __init__(self, *permissions: str):
        self._permissions = permissions

    def _extract_request_from_args(self, args, kwargs) -> Request:
        variants = list(args)
        if "request" in kwargs:
            variants.append(kwargs["request"])

        variants = [v for v in variants if isinstance(v, Request)]
        assert len(variants) == 1, PermissionDeniedException(
            "Не удалось проверить права"
        )
        return variants[0]

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            request = self._extract_request_from_args(args, kwargs)

            for permission in self._permissions:
                if not request.user.has_perm(permission):
                    msg = "You do not have permission for that action."
                    if settings.DEBUG:
                        msg += f"\nPermission: {permission}"
                    raise PermissionDeniedException(msg)

            return func(*args, **kwargs)

        return wrapper


require_permission = RequirePermission


class PermissionsListMixin:
    choices: list[tuple[str, str]]

    @classproperty
    def permissions(self):
        return [
            (permission.split(".", 1)[-1], description)
            for permission, description in self.choices
        ]
