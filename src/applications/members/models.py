from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q

from applications.common.exceptions import PermissionDeniedException
from applications.common.file_uploader import upload_file
from applications.members.enums import ParticipationRequestState
from applications.members.model_permissions import ParticipationRequestPermissions


class User(AbstractUser):
    email = models.EmailField(blank=False, null=False, unique=True)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    middle_name = models.CharField(max_length=150, blank=True, null=True)
    phone_number = models.CharField(max_length=64, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)

    is_filled_by_user = models.BooleanField(default=False)

    @property
    def name(self):
        if not self.is_filled_by_user:
            return f"{self.username} <{self.email}>"
        return f"{self.last_name} {self.first_name} {self.middle_name}"

    def __str__(self):
        return f"User {self.id}: {self.name}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Notification(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    title = models.CharField(max_length=64)
    text = models.TextField()
    image = models.ImageField(upload_to=upload_file, blank=True, null=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification {self.id}: {self.title}"

    class Meta:
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"


class ParticipationRequestQuerySet(models.QuerySet["ParticipationRequest"]):
    def filter_active(self, user: User | None = None):
        qs = self.filter(
            state=ParticipationRequestState.PENDING,
        )
        if user:
            qs = qs.filter(Q(user=user))
        return qs


class ParticipationRequest(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="participation_requests",
    )
    authors = models.TextField()
    title = models.CharField(max_length=64)
    text = models.TextField()
    media = models.FileField(upload_to=upload_file)
    state = models.CharField(
        max_length=64,
        choices=ParticipationRequestState.choices,
        default=ParticipationRequestState.PENDING,
    )
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_participation_requests",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    permissions = ParticipationRequestPermissions
    objects = ParticipationRequestQuerySet.as_manager()

    def __str__(self):
        return f"Participation request {self.id} ({self.user}): {self.title}"

    class Meta:
        verbose_name = "Заявка на участие в конференции"
        verbose_name_plural = "Заявки на участие в конференции"
        permissions = ParticipationRequestPermissions.permissions
