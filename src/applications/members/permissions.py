from rest_framework.permissions import BasePermission


class IsFilledProfile(BasePermission):
    message = "Чтобы получить полный доступ к приложению необходимо заполнить профиль."

    def has_permission(self, request, view) -> bool:
        return request.user.is_filled_by_user
