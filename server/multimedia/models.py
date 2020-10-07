from django.db import models
from users.models import User
from channels.models import Channel
from django_extensions.db.models import TimeStampedModel
from django.utils.html import mark_safe

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

    def __str__(self):
        return self.user.username


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

    def __str__(self):
        return self.user.username


class Tags(TimeStampedModel):
    name = models.CharField(max_length=100, null=False, blank=True, unique=True)
    # ManyToManyRel = Media

    def total_videos(self):
        return self.video.all().count()

    total_videos.short_description = "Videos"

    def total_audios(self):
        return self.audio.all().count()

    total_audios.short_description = "Audios"

    def total_pictures(self):
        return self.picture.all().count()

    total_pictures.short_description = "Pictures"

    def total_articles(self):
        return self.article.all().count()

    total_articles.short_description = "Articles"

    def __str__(self):
        return self.name


class Views(TimeStampedModel):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    ip = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return self.user.username


class Media(TimeStampedModel):
    """
    Base Model for all media i.e videos, audio and other
    """

    title = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    thumbnail = models.ImageField(
        upload_to="multimedia/thumbnail", null=True, blank=True
    )
    channel = models.ForeignKey(
        Channel, on_delete=models.CASCADE, blank=True, related_name="%(class)s"
    )
    comments = models.ManyToManyField(Comments, related_name="%(class)s")
    likes = models.ManyToManyField(Likes, related_name="%(class)s", blank=True)
    views = models.ManyToManyField(Views, related_name="%(class)s", blank=True)
    tags = models.ManyToManyField(Tags, related_name="%(class)s", blank=True)
    content = models.FileField(upload_to="multimedia", null=False, blank=True)

    def total_likes(self):
        return self.likes.all().count()

    total_likes.short_description = "Likes"

    def total_comments(self):
        return self.comments.all().count()

    total_comments.short_description = "Comments"

    def total_views(self):
        return self.views.all().count()

    def thumbnail_tag(self):
        from django.utils.html import mark_safe

        return mark_safe("<img src=%s height=250/>" % self.thumbnail.url)

    thumbnail_tag.short_description = "Preview"

    def __str__(self):
        return self.title

    class Meta:
        abstract = True


class Video(Media):
    """
    model for Videos
    """

    pass


class Audio(Media):
    """
    model for Audios
    """

    pass


class Picture(Media):
    """
    model fot Pictures
    """

    pass


class Article(Media):
    """
    model for Articles
    """

    body = models.TextField(null=False, blank=True)


class SavedMedia(TimeStampedModel):
    """
    Saved medias for user
    """

    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    video = models.ManyToManyField(
        Video, blank=True, related_name="saved_videos", through="SavedVideo"
    )
    picture = models.ManyToManyField(
        Picture, blank=True, related_name="saved_pictures", through="SavedPicture"
    )
    article = models.ManyToManyField(
        Article, blank=True, related_name="saved_articles", through="SavedArticle"
    )
    audio = models.ManyToManyField(
        Audio, blank=True, related_name="saved_audios", through="SavedAudio"
    )

    def total_videos(self):
        return self.video.all().count()

    total_videos.short_description = "Videos Saved"

    def total_audios(self):
        return self.audio.all().count()

    total_audios.short_description = "Audios Saved"

    def total_pictures(self):
        return self.picture.all().count()

    total_pictures.short_description = "Pictures Saved"

    def total_articles(self):
        return self.article.all().count()

    total_articles.short_description = "Articles saved"

    def __str__(self):
        return self.user.username


class SavedVideo(TimeStampedModel):
    """
    Intermediate models for managing saved videos
    """

    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    saved_to = models.ForeignKey(SavedMedia, on_delete=models.CASCADE)


class SavedPicture(TimeStampedModel):
    """
    Intermediate models for managing saved pictures
    """

    picture = models.ForeignKey(Picture, on_delete=models.CASCADE)
    saved_to = models.ForeignKey(SavedMedia, on_delete=models.CASCADE)


class SavedAudio(TimeStampedModel):
    """
    Intermediate models for managing saved audio
    """

    audio = models.ForeignKey(Audio, on_delete=models.CASCADE)
    saved_to = models.ForeignKey(SavedMedia, on_delete=models.CASCADE)


class SavedArticle(TimeStampedModel):
    """
    Intermediate models for managing saved article
    """

    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    saved_to = models.ForeignKey(SavedMedia, models.CASCADE)
