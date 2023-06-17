from django.shortcuts import get_object_or_404

from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from announcement.models import Announcement
from announcement.permissions import IsOwnerOrReadOnly
from announcement.permissions import IsOwner
from announcement.serializers import AnnouncementSerializer
from announcement.filter_classes import AnnouncementFilters
from rest_framework.exceptions import NotFound
from rest_framework.response import Response


class ListCreateAnnouncementAPIView(generics.ListCreateAPIView):
    """create a Announcement"""

    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SearchAnnouncementAPIView(generics.ListAPIView):
    """List of Announcement with search and filter, the search params  is 'query' """

    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    filterset_class = AnnouncementFilters
    search_fields = ['title', 'content', ]


class RetrieveUpdateDestroyAnnouncement(generics.RetrieveUpdateDestroyAPIView):
    """accept a announcement """

    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def patch(self, request, *args, **kwargs):
        request.data['accept'] = True
        return super().patch(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        # add user to list of people viewed this announcement, and update view_count
        if request.user not in obj.viewed_by.all():
            obj.view_count = obj.view_count + 1 if obj.view_count else 1
            obj.viewed_by.add(request.user)
            obj.save()
        return super().retrieve(request, *args, **kwargs)


class ViewCountAnnouncement(APIView):
    """
    post:
        create a comment for a post.

    """

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, reqeust, *args, **kwargs):
        obj = Announcement.objects.filter(id=kwargs['pk']).last()
        if not obj:
            raise NotFound
        else:
            return Response({'view_count': obj.view_count}, status=200)


class MyAnnouncementView(generics.ListAPIView):
    """user announcement"""
    serializer_class = AnnouncementSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Announcement.objects.filter(user=self.request.user)
