from django.db import models
from django.contrib.auth import get_user_model
from utils.timestampmodel import TimeStampedModel

User = get_user_model()


# Create your models here.
class Announcement(TimeStampedModel):
    """Model for Announcement"""

    title = models.CharField(max_length=250, blank=False, null=False)
    content = models.TextField()
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="announcement"
    )
    accept = models.BooleanField(default=False)
    viewed_by = models.ManyToManyField(
        User, blank=True, related_name='viewed_posts')
    view_count = models.IntegerField(blank=True, null=True, default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created", "-updated"]
