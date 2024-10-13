from django.urls import path, include

from applications.api import views

urlpatterns = [
    path("members/", include("applications.members.api.urls")),
    path("auth/", include("applications.jwtauth.api.urls")),
    path("conference/", views.active_conference),
]
