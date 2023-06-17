from django.urls import path
from .views import (
    RetrieveUpdateDestroyAnnouncement,
    SearchAnnouncementAPIView,
    ListCreateAnnouncementAPIView,
    ViewCountAnnouncement,
    MyAnnouncementView,
)


app_name = "api"

urlpatterns = [
    path("", ListCreateAnnouncementAPIView.as_view(), name='announcement-list'),
    path("<int:pk>/", RetrieveUpdateDestroyAnnouncement.as_view(),
         name='announcement-detail'),
    path("<int:pk>/views/", ViewCountAnnouncement.as_view(), name='view_count'),
    path('search/', SearchAnnouncementAPIView.as_view(),),
    path('my-announcements/', MyAnnouncementView.as_view(),
         name='my-announcements'),

]
