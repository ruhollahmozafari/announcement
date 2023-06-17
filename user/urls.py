"""Urls module for drf-user"""
from django.urls import path

from user import views


app_name = "user"


urlpatterns = [
    path("login/", views.LoginView.as_view(), name="Login"),
    # ex: api/user/register/
    path("sign-up/", views.RegisterView.as_view(), name="Sign-Up"),
    path(
        "profile/",
        views.RetrieveUpdateUserAccountView.as_view(),name = 'get_update_account'
    ),
]
