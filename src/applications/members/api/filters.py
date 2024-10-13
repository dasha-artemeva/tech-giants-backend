from django_filters import rest_framework as filters

from applications.members.enums import ParticipationRequestState


class ParticipationRequestFilterSet(filters.FilterSet):
    user = filters.NumberFilter(field_name="user_id")
    state = filters.ChoiceFilter(
        field_name="state", choices=ParticipationRequestState.choices
    )
