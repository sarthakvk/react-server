from django.contrib import admin
from .models import (
    Video,
    Audio,
    Article,
    Picture,
    SavedVideo,
    SavedAudio,
    SavedArticle,
    SavedPicture,
    SavedMedia,
    Tags,
)
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from os.path import splitext

# Register your models here.


class AdminMediaWidget(AdminFileWidget):
    def render(self, name, value, attrs=None, renderer=None):
        output = []
        media_type = {
            "video": ["mp4", "mov", "wmv", "ogg", "webm"],
            "audio": ["mp3", "wav"],
        }

        if value and getattr(value, "url", None):
            image_url = value.url
            ext = splitext(image_url)[1][1:]
            file_name = str(value)

            if ext in media_type["video"]:
                output.append(
                    u' <video controls height=200 alt="%s" ><source src="%s"></video> '
                    % (file_name, image_url)
                )

            elif ext in media_type["audio"]:
                output.append(
                    u' <audio controls height=200 alt="%s" ><source src="%s"></audio> '
                    % (file_name, image_url)
                )

            else:
                output.append(
                    u' <a href="%s" target="_blank"><img src="%s" height=200 alt="%s" /></a> %s '
                    % (image_url, image_url, file_name, _("Change:"))
                )

        output.append(super(AdminFileWidget, self).render(name, value, attrs, renderer))
        return mark_safe(u"".join(output))


class MediaWidgetAdmin(admin.ModelAdmin):
    image_fields = []

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name in self.image_fields:
            request = kwargs.pop("request", None)
            kwargs["widget"] = AdminMediaWidget
            return db_field.formfield(**kwargs)
        return super(MediaWidgetAdmin, self).formfield_for_dbfield(db_field, **kwargs)


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = [
        "name",
        "total_videos",
        "total_audios",
        "total_pictures",
        "total_articles",
    ]


class MediaAdmin(MediaWidgetAdmin):
    exclude = (
        "comments",
        "likes",
        "views",
    )
    list_display = ("title", "channel", "total_views", "total_likes", "total_comments")
    filter_horizontal = ("tags",)
    autocomplete_fields = ["channel"]
    search_fields = ["title", "channel__name"]
    list_filter = ["channel"]
    ordering = ["-modified"]
    image_fields = ["thumbnail", "content"]


@admin.register(Video)
class VideoAdmin(MediaAdmin):
    pass


@admin.register(Audio)
class AudioAdmin(MediaAdmin):
    pass


@admin.register(Picture)
class PictureAdmin(MediaAdmin):
    pass


@admin.register(Article)
class ArticleAdmin(MediaAdmin):
    pass


class SavedVideoAdmin(admin.TabularInline):
    model = SavedVideo
    extra = 1


class SavedAudioAdmin(admin.TabularInline):
    model = SavedAudio
    extra = 1


class SavedPictureAdmin(admin.TabularInline):
    model = SavedPicture
    extra = 1


class SavedArticleAdmin(admin.TabularInline):
    model = SavedArticle
    extra = 1


@admin.register(SavedMedia)
class SavedMediaAdmin(admin.ModelAdmin):
    inlines = (SavedVideoAdmin, SavedAudioAdmin, SavedArticleAdmin, SavedPictureAdmin)
    search_fields = [
        "user__username",
        "video__title",
        "audio__title",
        "picture__title",
        "article__title",
    ]
    list_display = [
        "user",
        "total_videos",
        "total_audios",
        "total_pictures",
        "total_articles",
    ]
