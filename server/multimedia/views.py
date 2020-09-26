from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
)
from .serializer import GetLatestVideoSerializer
from .models import Video, Audio, Picture, Article
from main.tools import return_response

# Create your views here.


class GetLatestVideo(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        response_data = {}
        serializer = GetLatestVideoSerializer(data=request.data)
        if serializer.is_valid():
            count = serializer.validated_data.get("count")
            videos = Video.objects.all().order_by("-created")[:count]
            response_data["videos"] = videos
            format = {
                "videos": [
                    {
                        "id": 1,
                        "title": 1,
                        "description": 1,
                        "thumbnail": 1,
                    }
                ]
            }
        return return_response(response_data=response_data, format=format)
