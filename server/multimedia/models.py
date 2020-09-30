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
    # ManyToManyRel = Media


class Comments(TimeStampedModel):
    """
    Comments model for storing likes and dislikes
    this has many2many relation with `Media` model
    with `media` as related name.
    This model is also have one2many relation to `self`
    for reply and their reply and so on ...
    """

    message = models.TextField(null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    reply_to = models.ForeignKey(
        "self", related_name="replies", blank=True, null=True, on_delete=models.SET_NULL
    )
    # ManyToManyRel = Media


class Tags(TimeStampedModel):
    name = models.CharField(max_length=100, null=False, blank=True, unique=True)
    # ManyToManyRel = Media


class Views(TimeStampedModel):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)


class Media(TimeStampedModel):
    """
    Base Model for all media i.e videos, audio and other
    """

    MEDIA_TYPE = (
        ("video", "Video"),
        ("audio", "Audio"),
        ("picture", "Picture"),
        ("article", "Article"),
    )

    title = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=10, choices=MEDIA_TYPE, null=False, blank=False)
    thumbnail = models.ImageField(
        upload_to="multimedia/thumbnail", null=True, blank=True
    )
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, blank=True)
    comments = models.ManyToManyField(Comments, related_name="media")
    likes = models.ManyToManyField(Likes, related_name="media", blank=True)
    views = models.ManyToManyField(Views, related_name="media", blank=True)
    tags = models.ManyToManyField(Tags, related_name="media", blank=True)


class Video(Media):
    """
    model for Videos
    """

    content = models.FileField(upload_to="multimedia/videos", null=False, blank=False)


class Audio(Media):
    """
    model for Audios
    """

    content = models.FileField(upload_to="multimedia/audios", null=False, blank=False)


class Picture(Media):
    """
    model fot Pictures
    """

    content = models.FileField(upload_to="multimedia/pictures", null=False, blank=True)


class Article(Media):
    """
    model for Articles
    """

    content = models.FileField(upload_to="multimedia/article", null=True, blank=True)
    body = models.TextField(null=False, blank=True)


class SavedMedia(TimeStampedModel):
    """
    Saved medias for user
    """

    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    media = models.ManyToManyField(Media, blank=True, related_name="saved_to")
