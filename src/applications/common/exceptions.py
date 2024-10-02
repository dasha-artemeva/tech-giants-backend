class BaseServiceException(Exception):
    def __init__(self, detail: str | None = None):
        if detail is not None:
            self.detail = detail


class PermissionDeniedException(BaseServiceException):
    detail = "Permission Denied"
