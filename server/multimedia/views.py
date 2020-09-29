from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
)
from .serializer import (
    GetLatestVideoSerializer,
    GetVideosSerializer,
    AllMediaSerializer,
)
from .models import Video, Audio, Picture, Article, Media
from channels.models import Channel
from main.tools import return_response, CacheMixin

# Create your views here.


class GetLatestVideosHome(CacheMixin, APIView):
    """
    endpoint to get top videos on home page
    """

    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        response_data = {}
        serializer = GetLatestVideoSerializer(data=request.GET)
        if serializer.is_valid():
            count = serializer.validated_data.get("count")
            videos = Video.objects.all().order_by("-created")[:count]
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


class GetChannelVideos(CacheMixin, APIView):
    """
    endpoint to get channel wise videos on home page
    """

    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        response_data = {}
        response_maxlen = {}
        serializer = GetVideosSerializer(data=request.GET)
        if serializer.is_valid():
            start = (serializer.validated_data["page"] - 1) * 3
            channels = Channel.objects.all().order_by("name")[start : start + 3]
            response_data["channels"] = channels
            response_maxlen["videos"] = 10
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


class AllMedia(CacheMixin, APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_class(self, type):
        media_dict = {
            "video": Video,
            "article": Article,
            "picture": Picture,
            "audio": Audio,
        }
        return media_dict[type]

    def get_query_prefix(self, orderby):
        order_dict = {
            "time": ".prefetch_related('tags')" ".all().order_by('created')",
            "likes": ".prefetch_related('tags', 'likes')"
            ".annotate(total_likes=Count('likes'))"
            ".order_by('-total_likes')",
            "comments": "prefetch_related('tags', 'comments')"
            ".annotate(total_comments=Count('comments'))"
            ".order_by('-total_comments')",
            "views": ".prefetch_related('tags', 'views')"
            ".annotate(total_views=Count('views'))"
            ".order_by('-total_views')",
            "editor_choice": ".select_related('channel')"
            ".prefetch_related('tags', 'channel__subscribers')"
            ".annotate(subs=Count('channel__subscribers'))"
            ".order_by(-subs)",
        }
        return order_dict[orderby]

    def get(self, request):
        response_data = {}
        serializer = AllMediaSerializer(data=request.GET)

        if serializer.is_valid():
            tags = serializer.validated_data.get("tags")
            page = (serializer.validated_data.get("page") - 1) * 18
            type = serializer.validated_data.get("type")
            orderby = serializer.validated_data.get("orderby")

            media_class = self.get_class(type)

            response_data["total_length"] = media_class.objects.all().count()

            ordered_response = eval(
                "media_class.objects" + self.get_query_prefix(orderby)
            )

            if tags:
                ordered_response = ordered_response.filter(tags__in=tags)

            response_data["ordered_response"] = ordered_response[page : page + 18]

            response_format = {
                "ordered_response": [
                    {
                        "title": 1,
                        "description": 1,
                        "thumbnail": 1,
                    }
                ],
                "total_length": 1,
            }

        return return_response(response_data=response_data, format=response_format)
