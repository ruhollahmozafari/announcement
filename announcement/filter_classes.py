# some filter class that can be used for some models.
# you can yse this filterset for generic list view.
from django_filters import rest_framework as filters
from announcement.models import Announcement


class AnnouncementFilters(filters.FilterSet):
    """filter over posts with convering fk over user"""

    title__contains = filters.CharFilter(field_name="title", lookup_expr="contains")

    content__contains = filters.CharFilter(field_name="content", lookup_expr="contains")

    class Meta:
        model = Announcement
        fields = ["title"]
