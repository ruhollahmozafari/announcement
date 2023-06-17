import os
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers
from announcement.models import Announcement
from user.serializers import UserShowSerializer

User = get_user_model()


class AnnouncementSerializer(serializers.ModelSerializer):
    user = serializers.CurrentUserDefault()

    class Meta:
        model = Announcement
        exclude = ('viewed_by',)
        read_only_fields = ("user",)

