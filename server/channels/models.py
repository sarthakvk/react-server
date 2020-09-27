from django.db import models
from django.apps import apps
from users.models import User
from django_extensions.db.models import TimeStampedModel

# Create your models here.


class Channel(TimeStampedModel):
    """
    model for managing channels
    """

    name = models.CharField(max_length=100, null=False, blank=False)
    owner = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    profile_pic = models.ImageField(null=True, blank=True, upload_to="channels/profile")
    about = models.TextField(null=True, blank=True)
    subscribers = models.ManyToManyField(
        User, blank=True, related_name="channel_subscribed"
    )

    @property
    def videos(self):
        lazy_model = apps.get_model("multimedia", "Video")
        return lazy_model.objects.filter(media_ptr__type="video")
