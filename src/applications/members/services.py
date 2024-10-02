import datetime

from django.core.files import File
from django.db.models import Q

from applications.common.exceptions import BaseServiceException
from applications.members.contants import MAX_USER_REQUESTS
from applications.members.exceptions import AssignToNotModeratorException
from applications.members.models import User, ParticipationRequest
from applications.members.enums import ParticipationRequestState


def create_user(username: str, email: str, password: str) -> User:
    user_already_registered = User.objects.filter(
        Q(username=username) | Q(email=email)
    ).exists()
    if user_already_registered:
        raise BaseServiceException("Пользователь с такими данными уже существует")
    try:
        user = User.objects.create_user(
            username=username, email=email, password=password
        )
    except ValueError as e:
        raise BaseServiceException("Ошибка регистрации пользователя") from e
    return user


def update_user(
    user: User,
    first_name: str,
    last_name: str,
    middle_name: str,
    phone_number: str,
    birth_date: datetime.date,
) -> User:
    user.first_name = first_name
    user.last_name = last_name
    user.middle_name = middle_name
    user.phone_number = phone_number
    user.birth_date = birth_date
    user.is_filled_by_user = all(
        [
            user.first_name,
            user.last_name,
            user.middle_name,
            user.phone_number,
            user.birth_date,
        ]
    )
    user.save()
    return user


def create_participation_request(
    user: User, authors: str, title: str, text: str, media: File
) -> ParticipationRequestState:
    if (
        not user.has_perm(ParticipationRequest.permissions.MODERATOR)
        and ParticipationRequest.objects.filter_active(user=user).count()
        > MAX_USER_REQUESTS
    ):
        raise BaseServiceException(
            "Вы не можете создать заявку.\n"
            f"Максимальное количество заявок {MAX_USER_REQUESTS}"
        )
    participation_request = ParticipationRequest.objects.create(
        user=user,
        authors=authors,
        title=title,
        text=text,
        media=media,
        state=ParticipationRequestState.PENDING,
    )
    return participation_request


def update_participation_request(
    participation_request: ParticipationRequest,
    assigned_to: User | None = None,
    state: ParticipationRequestState | None = None,
) -> ParticipationRequest:
    if assigned_to:
        if not assigned_to.has_perm(ParticipationRequest.permissions.MODERATOR):
            raise AssignToNotModeratorException()
        participation_request.assigned_to = assigned_to
    if state:
        participation_request.state = state
    participation_request.save()
    return participation_request
