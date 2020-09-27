from django.urls import path
from .views import GetLatestVideo, GetVideos

app_name = "multimedia"

urlpatterns = [
    path("latest_videos/", GetLatestVideo.as_view(), name="latest_videos"),
    path("home_videos/", GetVideos.as_view(), name="home_videos"),
]
