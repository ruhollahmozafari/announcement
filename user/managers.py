"""Custom Managers for drf-user"""
from typing import Optional

from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    """
    UserManager class for Custom User Model

    Source: Can't find link but the following solution is inspired
    from a solution provided on internet.
    """

    use_in_migrations = True

    def _create_user(
        self,
        username: str,
        email: str,
        password: str,
        fullname: str,
        mobile: Optional[str] = None,
        **kwargs
    ):
        """
        Creates and saves a User with given details
        """
        email = self.normalize_email(email)
        user = self.model(
            username=username, email=email, name=fullname, mobile=mobile, **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(
        self,
        username: str,
        email: str,
        password: str,
        name: str,
        mobile: Optional[str] = None,
        **kwargs
    ):
        """
        Creates a normal user considering the specified user settings
        from Django Project's settings.py

        Parameters
        ----------
        username: str
        email: str
        password: str
        name: str
        mobile: str, optional
        kwargs

        Returns
        -------
        User Instance
        """
        kwargs.setdefault("is_superuser", False)
        kwargs.setdefault("is_staff", False)
        kwargs["is_active"] = True

        return self._create_user(username, email, password, name, mobile, **kwargs)

    def create_superuser(
        self,
        username: str,
        email: str,
        password: str,
        name: str,
        mobile: Optional[str] = None,
        **kwargs
    ):
        """
        Creates a super user considering the specified user settings
        from Django Project's settings.py
        Parameters
        ----------
        username: str
        email: str
        password: str
        name: str
        mobile: str, optional
        kwargs

        Returns
        -------
        User Instance
        """

        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("is_staff", True)
        kwargs["is_active"] = True

        if kwargs.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        if kwargs.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        return self._create_user(username, email, password, name, mobile, **kwargs)
