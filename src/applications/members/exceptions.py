from applications.common.exceptions import BaseServiceException


class AssignToNotModeratorException(BaseServiceException):
    detail = "Данный пользователь не может модерировать заявку."
