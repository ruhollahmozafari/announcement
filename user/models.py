"""Models for drf-user"""
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import Group
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.text import gettext_lazy as _

from user.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    Represents default user model in a Django project.
    Adds following extra attributes:
    mobile: Mobile Number of the user
    name: Name of the user. Replaces last_name & first_name
    update_date: DateTime instance when the user was updated
    """

    username = models.CharField(
        verbose_name=_("Unique UserName"), max_length=254, unique=True
    )
    email = models.EmailField(verbose_name=_("Email Address"), unique=True)
    mobile = models.CharField(
        verbose_name=_("Mobile Number"),
        max_length=150,
        unique=True,
        null=True,
        blank=True,
    )
    name = models.CharField(verbose_name=_("Full Name"), max_length=500, blank=False)
    profile_image = models.ImageField(
        verbose_name=_("Profile Photo"), upload_to="user_images", null=True, blank=True
    )
    date_joined = models.DateTimeField(verbose_name=_("Date Joined"), auto_now_add=True)
    update_date = models.DateTimeField(verbose_name=_("Date Modified"), auto_now=True)
    is_active = models.BooleanField(verbose_name=_("Activated"), default=False)
    is_staff = models.BooleanField(verbose_name=_("Staff Status"), default=False)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["name", "email"]

    class Meta:
        """Passing model metadata"""

        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def get_full_name(self) -> str:
        """Method to return user's full name"""

        return str(self.name)

    def __str__(self):
        """String representation of model"""

        return str(self.name) + " | " + str(self.username)
