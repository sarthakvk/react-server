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
    MediaPreviewSerializer,
)
from .models import Video, Audio, Picture, Article, Media, Views
from channels.models import Channel
from main.tools import return_response, CacheMixin, get_media_class
from ipware import get_client_ip
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
            channels = (
                Channel.objects.prefetch_related("video")
                .all()
                .annotate(max=Count("video"))
                .order_by("-max")[start : start + 3]
            )
            response_data["channels"] = channels
            response_maxlen["video"] = 10
            response_format = {
                "channels": [
                    {
                        "name": 1,
                        "profile_pic": 1,
                        "video": [
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
        TIME = ".prefetch_related('tags').all()" ".order_by('-created')"

        LIKES = (
            ".prefetch_related('tags', 'likes')"
            ".annotate(total_likes=Count('likes'))"
            ".order_by('-total_likes')"
        )

        COMMENTS = (
            "prefetch_related('tags', 'comments')"
            ".annotate(total_comments=Count('comments'))"
            ".order_by('-total_comments')"
        )

        EDITOR_CHOICE = (
            ".select_related('channel')"
            ".prefetch_related('tags', 'channel__subscribers')"
            ".annotate(subs=Count('channel__subscribers'))"
            ".order_by(-subs)"
        )

        order_dict = {
            "time": TIME,
            "likes": LIKES,
            "comments": COMMENTS,
            "editor_choice": EDITOR_CHOICE,
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
                        "id": 1,
                        "title": 1,
                        "description": 1,
                        "thumbnail": 1,
                    }
                ],
                "total_length": 1,
            }

            return return_response(response_data=response_data, format=response_format)
        return return_response(status=False)


class MediaPreview(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        response_data = {}
        serializer = MediaPreviewSerializer(data=request.GET)
        if serializer.is_valid():
            media_id = serializer.validated_data.get("id")
            type = serializer.validated_data.get("type")
            media_class = get_media_class(type)

            media = media_class.objects.prefetch_related(
                "comments", "likes", "views"
            ).get(id=media_id)
            response_data[type] = media
            response_data[
                "comments"
            ] = media.comments.all().annotate(replies_count=Count('replies')).order_by('-replies_count')
            response_data["likes_count"] = media.likes.filter(val=True).count()
            response_data["dislikes_count"] = media.likes.filter(val=False).count()
            response_data["views_count"] = media.views.all().count()
            response_data["liked"] = None
            if request.user.is_anonymous:
                ip, _ = get_client_ip(request)
                if ip:
                    view, is_created = Views.objects.get_or_create(user=None, ip=ip)
                    if is_created:
                        eval("view.{}.add(media)".format(type))
                        view.save()
            else:
                view, is_created = Views.get_or_create(user=request.user)
                if is_created:
                    eval("view.{}.add(media)".format(type))
                    view.save()
                has_responded = media.likes.filter(user=request.user)
                if has_responded:
                    response_data["liked"] = has_responded[0].val

            response_format = {
                type: {
                    "id": 1,
                    "title": 1,
                    "description": 1,
                    "thumbnail": 1,
                    "content": 1,
                    "body": 1,
                },
                "comments": [
                    {
                        "id": 1,
                        "message": 1,
                        "replies_count": 1,
                    }
                ],
                "likes_count": 1,
                "dislikes_count": 1,
                "liked": 1,
                "views_count": 1,
            }
        return return_response(response_data=response_data, format=response_format)
