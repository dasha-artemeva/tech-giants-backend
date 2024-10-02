from django.urls import path
from rest_framework.routers import SimpleRouter

from applications.jwtauth.api import views

urlpatterns = [
    path("register/", views.register),
    path("login/", views.login),
    path("user/", views.UserView.as_view()),
]
