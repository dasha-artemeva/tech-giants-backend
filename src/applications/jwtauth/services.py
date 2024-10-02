from rest_framework_simplejwt.tokens import AccessToken

from applications.common.exceptions import BaseServiceException
from applications.members.models import User


def login_user(*,
               password: str,
               email: str | None = None,
               username: str | None = None) -> tuple[User, AccessToken]:
    user = None
    if email:
        user = User.objects.filter(email=email).first()
    if user is None and username:
        user = User.objects.filter(username=username).first()
    if not user or not user.check_password(password):
        raise BaseServiceException("Invalid credentials")
    return user, AccessToken.for_user(user)
