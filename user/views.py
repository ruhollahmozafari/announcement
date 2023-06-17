from django.conf import settings
from django.utils.text import gettext_lazy as _
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.settings import api_settings
from user.models import User
from user.serializers import UserSerializer
from user.serializers import CustomTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    """
    Register View

    Register a new user to the system.
    The data required are username, email, name, password and mobile (optional).
    """

    serializer_class = UserSerializer

    def perform_create(self, serializer):
        """Override perform_create to create user"""
        data = {
            "username": serializer.validated_data["username"],
            "email": serializer.validated_data["email"],
            "name": serializer.validated_data["name"],
            "password": serializer.validated_data["password"],
            "mobile": serializer.validated_data.get("mobile", None),
        }
        return User.objects.create_user(**data)


class LoginView(APIView):
    """
    Login View

    This is used to Login into system.
    The data required are 'username' and 'password'.

    username -- Either username or mobile or email address.
    password -- Password of the user.
    """

    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        """
        Process a login request via username/password.
        """
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)

        # if data is valid then create a record in auth transaction model
        user = serializer.user
        token = serializer.validated_data.get("access")
        refresh_token = serializer.validated_data.get("refresh")

        # For backward compatibility, returning custom response
        # as simple_jwt returns `access` and `refresh`
        resp = {
            "refresh_token": str(refresh_token),
            "token": str(token),
            "session": user.get_session_auth_hash(),
        }
        return Response(resp, status=200)


class RetrieveUpdateUserAccountView(generics.RetrieveUpdateAPIView):
    """
    Retrieve Update User Account View

    get: Fetch Account Details
    put: Update all details
    patch: Update some details
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "created_by"

    def get_object(self):
        """Fetches user from request"""

        return self.request.user

    def update(self, request, *args, **kwargs):
        """Updates user's password"""

        response = super(RetrieveUpdateUserAccountView, self).update(
            request, *args, **kwargs
        )
        # we need to set_password after save the user otherwise it'll save the raw_password in db. # noqa
        if "password" in request.data.keys():
            self.request.user.set_password(request.data["password"])
            self.request.user.save()
        return response

