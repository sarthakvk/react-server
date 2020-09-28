from django.shortcuts import render
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
)
from .serializer import GetLatestVideoSerializer, GetVideosSerializer
from .models import Video, Audio, Picture, Article
from channels.models import Channel
from main.tools import return_response, CacheMixin

# Create your views here.


class GetLatestVideo(CacheMixin ,APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        response_data = {}
        serializer = GetLatestVideoSerializer(data=request.GET)
        if serializer.is_valid():
            count = serializer.validated_data.get("count")
            videos = Video.objects.all().order_by("-created")[
                :count
            ]
            response_data["videos"] = videos
            response_format = {
                "videos": [
                    {
                        "id": 1,
                        "title": 1,
                        "description": 1,
                        "thumbnail": 1,
                    },
                ],
            }
        return return_response(response_data=response_data, format=response_format)


class GetVideos(CacheMixin, APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        response_data = {}
        response_maxlen = {}
        serializer = GetVideosSerializer(data=request.GET)
        if serializer.is_valid():
            start = (serializer.validated_data["page"] - 1) * 3
            channels = Channel.objects.all().order_by("name")[
                start : start + 3
            ]
            response_data["channels"] = channels
            response_maxlen["videos"] = 10000
            response_format = {
                "channels": [
                    {
                        "name": 1,
                        "profile_pic": 1,
                        "videos": [
                            {
                                "id": 1,
                                "title": 1,
                                "description": 1,
                                "thumbnail": 1,
                            },
                        ],
                    },
                ],
            }
            return return_response(
                response_data=response_data,
                format=response_format,
                response_maxlen=response_maxlen,
            )
        return return_response(status=False)
