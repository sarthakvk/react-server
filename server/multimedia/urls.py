from django.urls import path
from .views import GetLatestVideo

app_name = "multimedia"

urlpatterns = [
    path("latest_videos/", GetLatestVideo.as_view(), name="latest_videos"),
]
