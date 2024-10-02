from django.db import models

from applications.common.permissions import PermissionsListMixin


class ParticipationRequestPermissions(PermissionsListMixin, models.TextChoices):
    MODERATOR = (
        "members.moderator_participationrequest",
        "Модератор заявок на участие в конференции",
    )
