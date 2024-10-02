from django.db import models


class NotificationType(models.TextChoices):
    INFO = "info"
    ACCOUNT = "account"


class ParticipationRequestState(models.TextChoices):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
