from django.db import models
from users.models import User
from channels.models import Channel
from django_extensions.db.models import TimeStampedModel

# Create your models here.


class Likes(TimeStampedModel):
    """
    Like model for storing likes and dislikes
    this has many2many relation with `Media` model
    with `media` as related name
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    val = models.BooleanField(null=False, blank=False)


class Comments(TimeStampedModel):
    """
    Comments model for storing likes and dislikes
    this has many2many relation with `Media` model
    with `media` as related name.
    This model is also have many2many relation to `self`
    for reply and their reply and so on ...
    """

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    reply = models.ManyToManyField("self", blank=True, related_name="parent")


class Media(TimeStampedModel):
    """
    Base Model for all media i.e videos, audio and other
    """

    title = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    thumbnail = models.ImageField(
        upload_to="multimedia/thumbnail", null=True, blank=True
    )
    comments = models.ManyToManyField(Comments, related_name="media")
    likes = models.ManyToManyField(Likes, related_name="media", blank=True)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, blank=True)


class Video(Media):
    """
    model for Videos
    """

    link = models.FileField(upload_to="multimedia/videos", null=False, blank=False)


class Audio(Media):
    """
    model for Audios
    """

    link = models.FileField(upload_to="multimedia/audios", null=False, blank=False)


class Picture(Media):
    """
    model fot Pictures
    """

    link = models.FileField(upload_to="multimedia/pictures", null=False, blank=True)


class Article(Media):
    """
    model for Articles
    """

    image = models.FileField(upload_to="multimedia/article", null=True, blank=True)
    content = models.TextField(null=False, blank=True)
