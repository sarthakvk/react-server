from django.urls import path
from .views import (
    GetLatestVideosHome,
    GetChannelVideos,
    AllMedia,
    MediaPreview,
    GetTags,
)

app_name = "multimedia"

urlpatterns = [
    path("latest_videos/", GetLatestVideosHome.as_view(), name="latest_videos"),
    path("home_videos/", GetChannelVideos.as_view(), name="home_videos"),
    path("all_media/", AllMedia.as_view(), name="all_media"),
    path("view_media/", MediaPreview.as_view(), name="media_preview"),
    path("get_media_tags/", GetTags.as_view(), name="get_tag"),
]
