from django.contrib import admin
from .models import Video, Audio, Article, Picture

# Register your models here.


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    exclude = ("comments", "likes")


@admin.register(Audio)
class AudioAdmin(admin.ModelAdmin):
    exclude = ("comments", "likes")


@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    exclude = ("comments", "likes")


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    exclude = ("comments", "likes")
