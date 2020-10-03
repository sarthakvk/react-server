from rest_framework import serializers


class GetLatestVideoSerializer(serializers.Serializer):
    count = serializers.IntegerField(required=False, default=3)


class GetVideosSerializer(serializers.Serializer):
    page = serializers.IntegerField(required=True)


class AllMediaSerializer(serializers.Serializer):
    ORDER = (
        ("time", "Time"),
        ("likes", "Likes"),
        ("comments", "Comments"),
        ("views", "Views"),
        ("editor_choice", "Editor Choice"),
    )

    TYPE = (
        ("video", "Video"),
        ("audio", "Audio"),
        ("picture", "Picture"),
        ("article", "Article"),
    )
    type = serializers.ChoiceField(required=True, choices=TYPE)
    page = serializers.IntegerField(required=True)
    orderby = serializers.ChoiceField(required=True, choices=ORDER)
    tags = serializers.ListField(required=False)


class MediaPreviewSerializer(serializers.Serializer):
    TYPE = (
        ("video", "Video"),
        ("audio", "Audio"),
        ("picture", "Picture"),
        ("article", "Article"),
    )
    id = serializers.IntegerField(required=True)
    type = serializers.ChoiceField(required=True, choices=TYPE)


class GetTagSerializer(serializers.Serializer):
    TYPE = (
        ("video", "Video"),
        ("audio", "Audio"),
        ("picture", "Picture"),
        ("article", "Article"),
    )
    type = serializers.ChoiceField(required=True, choices=TYPE)
