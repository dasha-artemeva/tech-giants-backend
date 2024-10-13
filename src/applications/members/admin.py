from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from applications.members.exceptions import AssignToNotModeratorException
from applications.members.models import User, Notification, ParticipationRequest
from applications.members.enums import ParticipationRequestState


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "email", "password", "is_filled_by_user")}),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "middle_name",
                    "name",
                    "phone_number",
                    "birth_date",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )
    readonly_fields = ("name", "id")
    search_fields = (
        "username",
        "first_name",
        "last_name",
        "middle_name",
        "email",
        "phone_number",
    )


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "is_read")
    list_filter = ("is_read", "user")
    search_fields = ("title", "text", "user__username", "user__email")

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("user")


@admin.register(ParticipationRequest)
class ParticipationRequestAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "state")
    list_filter = ("state", "user", "assigned_to")
    search_fields = ("title", "text", "user__username", "user__email")
    autocomplete_fields = ("user", "assigned_to")

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("user", "assigned_to")

    def save_related(self, request, form, formsets, change):
        if "assigned_to" in form.changed_data:
            if not form.cleaned_data["assigned_to"].has_perm(
                ParticipationRequest.permissions.MODERATOR
            ):
                return messages.error(request, AssignToNotModeratorException.detail)
        super().save_related(request, form, formsets, change)
